import logging
import os
import json
import datetime

class Audiobook:
    def __init__(self, title, url):
        if not title or not url:
            raise ValueError('Audiobook title or url is not set.')
        self.title = title
        self.url = url
        self.directory = self.make_dir()
        self.chapters = []
        self.youtube_comment = ''

    def make_dir(self):
        try:
            if not self.title:
                raise ValueError('Audiobook title is not set.')

            directory_for_audiobook = f'./audiobooks/{self.title}'
            logging.info(f'Creating directory audiobook [{directory_for_audiobook}] if it does not exist already.')
            os.makedirs(directory_for_audiobook, exist_ok=True)

            return directory_for_audiobook
        except Exception as e:
            logging.error(f"An error occurred while creating the directory for Youtube data. ERROR: {e}")

    def find_chapters(self):
        logging.info(f'Finding chapters for [{self.title}].')
        audio_to_text_data = self.get_audio_to_text_data()

        self.find_chapters_from_audio_to_text_data(audio_to_text_data)
        self.calc_chapter_duration()

        self.youtube_comment = self.parse_chapters_to_youtube_comment_format()

    def get_audio_to_text_data(self):
        try:
            with open(f'{self.directory}/audio-to-text.json', 'r') as json_file:
                audio_to_text_data = json.load(json_file)
                return audio_to_text_data
        except Exception as e:
            logging.error(f"An error occurred while getting `audio-to-text.json` file. ERROR: {e}")

    def find_chapters_from_audio_to_text_data(self, audio_to_text_data):
        segments = audio_to_text_data['segments']
        chapters = []
        for segment in segments:
            if self.segment_contain_chapter(segment['text']):
                chapter = {
                    'title': f'Chapter {len(chapters)+1}',
                    'start': segment['start']
                }
                chapters.append(chapter)
        self.chapters = chapters

    # TODO: Add support to more languages
    def segment_contain_chapter(self, text):
        text = text.lower()
        return 'cap\u00edtulo' in text or 'capítulo' in text or 'chapter' in text

    def calc_chapter_duration(self):
        for i in range(len(self.chapters)):
            if i == 0:
                self.chapters[i]['duration'] = self.chapters[i]['start']
                continue
            self.chapters[i]['duration'] = self.chapters[i]['start'] - self.chapters[i-1]['start']

    def parse_chapters_to_youtube_comment_format(self):
        logging.info("Parsing chapters to youtube comment format...")
        youtube_comment = []
        for i in range(len(self.chapters)):
            chapter_title =self. chapters[i]['title']
            chapter_start_in_seconds = self.chapters[i]['start']
            chapter_start_at = self.seconds_to_time(chapter_start_in_seconds)
            chapter_duration = self.seconds_to_time(self.chapters[i]['duration'])

            youtube_comment.append({
                'chapter_title': chapter_title,
                'chapter_start_at': chapter_start_at,
                'chapter_duration': chapter_duration
            })

        youtube_comment_str = f'__________________\nResult for {self.title}\n{self.url}\n\n'
        for chapter in youtube_comment:
            youtube_comment_str += f"{chapter['chapter_title']} \t {chapter['chapter_start_at']} \t Duration: {chapter['chapter_duration']}\n"
        youtube_comment_str += '\n\nby https://github.com/ThisIsDjonathan/youtube-audiobook-chapter-identifier\n__________________'
        return youtube_comment_str

    def seconds_to_time(self, seconds):
        return str(datetime.timedelta(seconds=int(seconds)))

