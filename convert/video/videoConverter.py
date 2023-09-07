from convert.Converter import Converter
from pytube import YouTube
from enum import Enum
from pprint import pprint
import os
import whisper

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
            print(str(percentageOfCompletion) + "% downloaded")
        try:
            # Create a YouTube object
            yt = YouTube(self.path)

            # Select the video to download
            video = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
            yt.register_on_progress_callback(on_progress)
            print(f"Fetching \"{video.title}\"..")
            print(f"Fetching successful\n")
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
            self.localPath = os.path.join(self.config.tmpDir, filename)

        except Exception as e:
            raise YouTubeDownloadError(f"Error downloading from YouTube: {str(e)}")

    def downloadFromBilibili(self):
        try:
            # Download logic
            pass
        except Exception as e:
            raise BilibiliDownloadError(f"Error downloading from Bilibili: {str(e)}")

    def downloadFromUrl(self):
        try:
            # Download logic
            pass
        except Exception as e:
            raise UrlDownloadError(f"Error downloading from URL: {str(e)}")

    def download(self):
        try:
            super().download()
        except (DownloadError, VideoConverterError) as e:
            print(f"An error occurred during download: {str(e)}")

    def _convert(self):
        model_name = "base"
        print("Transcribing...", self.localPath)
        print("Using model:", model_name)
        model = whisper.load_model(model_name)
        result = model.transcribe(self.localPath)
        pprint(result)

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