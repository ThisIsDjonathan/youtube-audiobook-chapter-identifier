from pytube import YouTube
import logging
import os

class YoutubeVideoHandler:
    def __init__(self, audiobook):
        if not audiobook.title or not audiobook.url:
            raise ValueError('Audiobook title or url is not set.')
        self.youtube = YouTube(audiobook.url)
        self.youtube.register_on_progress_callback(self.log_download_progress_function)
        self.audiobook_title = audiobook.title
        self.audiobook_directory = audiobook.directory
        self.youtube_content_filename = 'youtube-content.mp4' #self.audiobook_title + '.mp4'

    def download(self):
        try:
            if self.youtube_data_exists():
                logging.info(f'Youtube content already exists for [{self.audiobook_title}]. Skipping this step...')
                return
            logging.info(f'Downloading Youtube content from [{self.audiobook_title}].')
            audio = self.youtube.streams.get_audio_only()
            audio.download(output_path=self.audiobook_directory, filename=self.youtube_content_filename)
            logging.info(f'Youtube content download is done.')
        except Exception as e:
            logging.error(f"An error occurred while downloading the Youtube content. ERROR: {e}")

    def youtube_data_exists(self):
        return os.path.exists(f'{self.audiobook_directory}/{self.youtube_content_filename}')


    def log_download_progress_function(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = round(bytes_downloaded / total_size * 100)
        logging.info(f"Downloaded {percentage_of_completion}% of the video")
