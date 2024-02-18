from pytube import YouTube
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    percentage_of_completion = round(bytes_downloaded / total_size * 100)
    logging.info(f"Downloaded {percentage_of_completion}% of the video")

def download_youtube_video(url, path):
    youtube = YouTube(url)
    youtube.register_on_progress_callback(progress_function)
    video = youtube.streams.get_highest_resolution()
    video.download(path)

# Use the function
download_youtube_video('https://www.youtube.com/watch?v=dQw4w9WgXcQ', './')