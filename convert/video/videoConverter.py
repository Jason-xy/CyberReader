from convert.Converter import Converter
from bilix.sites.bilibili import DownloaderBilibili
from bilix.progress.cli_progress import CLIProgress
from pytube import YouTube
from enum import Enum
from tqdm import tqdm
import asyncio
import requests
import whisper
import subprocess
import os

class videoPathType(Enum):
    YouTube = 0
    Bilibili = 1
    Url = 2
    File = 3
    Unknown = 4

class videoConverter(Converter):
    def __init__(self, config):
        super().__init__(config)
        self.pathType = None

    def findPathType(self):
        if self.path.startswith('https://www.youtube.com/watch?v='):
            self.pathType = videoPathType.YouTube
        elif self.path.startswith('https://www.bilibili.com/video/'):
            self.pathType = videoPathType.Bilibili
        elif self.path.startswith('http'):
            self.pathType = videoPathType.Url
        elif self.path.endswith('.mp4') or self.path.endswith('.mkv') or self.path.endswith('.flv'):
            self.pathType = videoPathType.File
        else:
            self.pathType = videoPathType.Unknown

    def _download(self):
        try:
            if self.pathType == videoPathType.YouTube:
                self.downloadFromYouTube()
            elif self.pathType == videoPathType.Bilibili:
                self.downloadFromBilibili()
            elif self.pathType == videoPathType.Url:
                self.downloadFromUrl()
            elif self.pathType == videoPathType.File:
                self.localPath = self.path
            else:
                raise VideoConverterPathTypeError('Unknown path type! Only YouTube, Bilibili, Url, and File are supported.')
        except Exception as e:
            print(f"An error occurred during download: {str(e)}")
            raise DownloadError(f"Error downloading video: {str(e)}")

    def downloadFromYouTube(self):
        def on_progress(stream, chunk, bytesRemaining):
            totalSize = stream.filesize
            bytesDownloaded = totalSize - bytesRemaining
            percentageOfCompletion = bytesDownloaded / totalSize * 100
            progress_bar.update(percentageOfCompletion)

        try:
            # Create a YouTube object
            yt = YouTube(self.path)

            # Register the progress callback function
            yt.register_on_progress_callback(on_progress)

            # Select the video to download
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()

            # Initialize the total file size for the progress bar
            totalSize = video.filesize

            # Initialize the progress bar
            progress_bar = tqdm(total=totalSize, unit='B', unit_scale=True)

            print(f"Fetching \"{video.title}\"..")
            print("Fetching successful\n")
            print(f"Information: \n"
                f"File size: {round(video.filesize * 0.000001, 2)} MegaBytes\n"
                f"Highest Resolution: {video.resolution}\n"
                f"Author: {yt.author}")
            print("Views: {:,}\n".format(yt.views))
            print(f"Downloading \"{video.title}\"..")

            # Get video filename
            filename = video.default_filename

            # Start the video download
            video.download(self.config.tmpDir)

            # Full path to the downloaded video
            self.localPath = os.path.join(os.path.abspath(self.config.tmpDir), filename)

            # Close the progress bar
            progress_bar.close()

        except Exception as e:
            raise YouTubeDownloadError(f"Error downloading from YouTube: {str(e)}")

    def downloadFromBilibili(self):
        async def biliDownload():
            async with DownloaderBilibili() as d:
                await d.get_video(self.path, self.config.tmpDir, only_audio=True)
        try:
            CLIProgress.start()
            asyncio.run(biliDownload())

            # TODO:How to get the filename?
            # Workaround: get the filename from directory
            filename = os.listdir(self.config.tmpDir)[0]
            self.localPath = os.path.join(os.path.abspath(self.config.tmpDir), filename)
        except Exception as e:
            raise BilibiliDownloadError(f"Error downloading from Bilibili: {str(e)}")

    def downloadFromUrl(self):
        try:
            if self.path.endswith('.m3u8'):
                filename = self.path.split('/')[-1].replace('.m3u8', '.mp4')
                self.localPath = os.path.join(os.path.abspath(self.config.tmpDir), filename)
                downloadAndConvertToMp4(self.path, self.localPath, os.path.abspath(self.config.tmpDir))
            else:
                response = requests.get(self.path, stream=True)
                filename = 'video'
                self.localPath = os.path.join(os.path.abspath(self.config.tmpDir), filename)
                if response.status_code == requests.codes.ok:
                    total_size = int(response.headers.get('Content-Length', 0))
                    block_size = 1024  # 1 KB
                    progress_bar = tqdm(total=total_size, unit='B', unit_scale=True)

                    with open(self.localPath, 'wb') as file:
                        for data in response.iter_content(block_size):
                            file.write(data)
                            progress_bar.update(len(data))
                    progress_bar.close()

        except Exception as e:
            raise UrlDownloadError(f"Error downloading from URL: {str(e)}")

    def download(self):
        try:
            super().download()
        except (DownloadError, VideoConverterError) as e:
            print(f"An error occurred during download: {str(e)}")

    def _convert(self):
        model_name = "base" # {tiny.en,tiny,base.en,base,small.en,small,medium.en,medium,large-v1,large-v2,large}]
        print("Transcribing...", self.localPath)
        print("Using model:", model_name)
        model = whisper.load_model(model_name)
        result = model.transcribe(self.localPath)
        self.text = result['text']

    def convert(self):
        try:
            super().convert()
        except VideoConverterError as e:
            print(f"An error occurred during conversion: {str(e)}")

    def _process(self):
        self.findPathType()
        self.download()
        self.convert()

    def process(self):
        try:
            super().process()
        except VideoConverterError as e:
            print(f"An error occurred during processing: {str(e)}")

# m3u8 functions
def downloadTsFiles(url, tmpDir):
    response = requests.get(url)
    response.raise_for_status()
    m3u8Content = response.text

    tsFiles = []
    lines = m3u8Content.split('\n')
    for line in lines:
        if line.endswith('.ts'):
            tsFiles.append(line)

    for i, tsFile in tqdm(enumerate(tsFiles), desc="Downloading files", total=len(tsFiles)):
        tsUrl = url.rsplit('/', 1)[0] + '/' + tsFile
        response = requests.get(tsUrl)
        response.raise_for_status()
        with open(os.path.join(tmpDir, f'temp_{i}.ts'), 'wb') as file:
            file.write(response.content)

    return tsFiles

def concatenateTsFiles(tsFiles, outputFile, tmpDir):
    with open(os.path.join(tmpDir, 'concatList.txt'), 'w') as f:
        for i in range(len(tsFiles)):
            f.write(f"file '{os.path.join(tmpDir, f'temp_{i}.ts')}'\n")
    cmd = f'ffmpeg -f concat -safe 0 -i "{os.path.join(tmpDir, "concatList.txt")}" -c copy {outputFile}'
    subprocess.call(cmd, shell=True)

def downloadAndConvertToMp4(url, outputFile, tmpDir):
    tsFiles = downloadTsFiles(url, tmpDir)
    concatenateTsFiles(tsFiles, outputFile, tmpDir)
    print('Video download and conversion completed!')

# Error handling
class DownloadError(Exception):
    pass

class YouTubeDownloadError(DownloadError):
    pass

class BilibiliDownloadError(DownloadError):
    pass

class UrlDownloadError(DownloadError):
    pass

class VideoConverterError(Exception):
    pass

class VideoConverterPathTypeError(VideoConverterError):
    pass