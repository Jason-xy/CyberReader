import requests
import subprocess
import os
from tqdm import tqdm

current_dir = os.path.dirname(os.path.abspath(__file__))
tmp_dir = os.path.join(current_dir, 'tmp')

def download_ts_files(url):
    response = requests.get(url)
    response.raise_for_status()
    m3u8_content = response.text

    ts_files = []
    lines = m3u8_content.split('\n')
    for line in lines:
        if line.endswith('.ts'):
            ts_files.append(line)

    for i, ts_file in tqdm(enumerate(ts_files), desc="Downloading files", total=len(ts_files)):
        ts_url = url.rsplit('/', 1)[0] + '/' + ts_file
        response = requests.get(ts_url)
        response.raise_for_status()
        with open(os.path.join(tmp_dir, f'temp_{i}.ts'), 'wb') as file:
            file.write(response.content)

    return ts_files

def concatenate_ts_files(ts_files, output_file):
    with open(os.path.join(tmp_dir, 'concat_list.txt'), 'w') as f:
        for i in range(len(ts_files)):
            f.write(f"file '{os.path.join(tmp_dir, f'temp_{i}.ts')}'\n")
    cmd = f'ffmpeg -f concat -safe 0 -i "{os.path.join(tmp_dir, "concat_list.txt")}" -c copy {output_file}'
    subprocess.call(cmd, shell=True)

def download_and_convert_to_mp4(url, output_file):
    # Create the 'tmp' directory for temporary files
    os.makedirs(tmp_dir, exist_ok=True)

    ts_files = download_ts_files(url)
    concatenate_ts_files(ts_files, output_file)

    # Remove the temporary ts files and the 'tmp' directory
    for file_name in os.listdir(tmp_dir):
        file_path = os.path.join(tmp_dir, file_name)
        os.remove(file_path)
    os.rmdir(tmp_dir)
    print('Cleanup completed!')

# Download and convert the ts files from the m3u8 URL to mp4 format
video_url = 'https://1500023114.vod-qcloud.com/183bcc5avodtranshk1500023114/959ef2dc5576678022427114301/video_1446006_0.m3u8'
output_file = os.path.join(os.getcwd(), 'video.mp4')
download_and_convert_to_mp4(video_url, output_file)

print('Video download and conversion completed!')