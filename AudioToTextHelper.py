import logging
import os
import whisper
import json

class AudioToTextHelper:
    def __init__(self, audiobook):
        if not audiobook.title or not audiobook.url:
            raise ValueError('Audiobook title or url is not set.')
        self.audiobook_title = audiobook.title
        self.audiobook_directory = audiobook.directory
        self.audio_to_text_filename = 'audio-to-text.json'
        self.audiobook_text = ''

    def audio_to_text(self):
        try:
            logging.info("\n\n")
            logging.info("Converting audio-to-text.")

            if self.audio_to_text_already_exists():
                logging.info(f'Text `{self.audio_to_text_filename}` file already exists. Skipping audio-to-text conversion.')
                logging.info(f'To transcribe again, delete the `{self.audio_to_text_filename}` file on `{self.audiobook_directory}`')
                return
            else:
                logging.info("This can take a while...\n\n")

            audio_file_path = f'{self.audiobook_directory}/youtube-content.mp4'
            logging.info(f"Transcribing audio file `{audio_file_path}`\n")

            model = whisper.load_model('base')
            self.audiobook_text = model.transcribe(audio_file_path)
        except Exception as e:
            logging.error(f"An error occurred while converting audio to text. ERROR: {e}")

    def audio_to_text_already_exists(self):
        return os.path.exists(f'{self.audiobook_directory}/{self.audio_to_text_filename}')

    def save_text_to_file(self):
        try:
            if self.audio_to_text_already_exists():
                return
            if self.audiobook_text is None or self.audiobook_text == '':
                logging.info("No text to save.")
            audiobook_text_json = json.dumps(self.audiobook_text, indent=4, ensure_ascii=False)

            file_folder_full_path = './audiobooks/' + self.audiobook_title
            os.makedirs(file_folder_full_path, exist_ok=True)

            audiobook_text_filename = f'{file_folder_full_path}/{self.audio_to_text_filename}'
            with open(audiobook_text_filename, 'w', encoding='utf-8') as file:
                file.write(audiobook_text_json)
        except Exception as e:
            logging.error(f"An error occurred while saving the text to file. ERROR: {e}")