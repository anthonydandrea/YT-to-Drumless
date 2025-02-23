from musicai_sdk import MusicAiClient
from dotenv import load_dotenv
import os
import yt_dlp
import ffmpeg
import argparse
import tempfile
import random
import string
import requests


parser = argparse.ArgumentParser(description="Convert Youtube video audio into a drumless mp3 file.")
parser.add_argument("--uri", type=str, help="Youtube video uri")
parser.add_argument("--out", type=str, help="Directory to output audio file")

args = parser.parse_args()
load_dotenv()

ydl_opts = {
    'quiet': True,
    'extract_flat': True,  # Only get video metadata, not download
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info_dict = ydl.extract_info(args.uri, download=False)
    video_title = info_dict['title'].replace(" ", "_")

musicai_api_key = os.getenv("MUSICAI_API_KEY")
client = MusicAiClient(api_key=musicai_api_key)

# Get application info
app_info = client.get_application_info()

with tempfile.TemporaryDirectory() as temp_dir:
    temp_filename = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    temp_out = os.path.join(temp_dir, temp_filename)
    print(temp_out)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": temp_out,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.uri])

    file_url = client.upload_file(file_path=temp_out + '.mp3')
    print('File Url:', file_url)

# Create Job
workflow_params = {
    'inputUrl': file_url,
}
create_job_info = client.create_job(job_name='test-job', workflow_id='drums-removal',params=workflow_params)
job_id = create_job_info['id']
print('Job Created:', job_id)

# Wait for job to complete
job_info = client.wait_for_job_completion(job_id)
print('Job Status:', job_info['status'])
print('Job Result:', job_info['result'])

# Get job info
job_info = client.get_job(job_id=job_id)
print('Job Status:', job_info['status'])
print('Job Result:', job_info['result'])

processed_audio_uri = job_info.get('result', {}).get('uri')

if processed_audio_uri is None:
    print("Something went wrong.")
    exit(1)

outfile = os.path.join(args.out, video_title + '.mp3')
with requests.get(processed_audio_uri, stream=True) as response:
    with open(outfile, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

print("File written:", outfile)

