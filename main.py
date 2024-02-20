from YoutubeContentHelper import YoutubeVideoHandler
from AudioToTextHelper import AudioToTextHelper
from Audiobook import Audiobook
import logging

def main():
    audiobook = Audiobook('The Animal Farm', 'https://www.youtube.com/watch?v=iosHzNmVYbA')

    # 1 - Download from Youtube
    youtube = YoutubeVideoHandler(audiobook)
    youtube.download()

    # 2 - Speech to Text
    audio_to_text = AudioToTextHelper(audiobook)
    audio_to_text.audio_to_text()
    audio_to_text.save_text_to_file()

    # 3 - Chapter Finder
    audiobook.find_chapters()
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()