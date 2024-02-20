from YoutubeContentHelper import YoutubeVideoHandler
from AudioToTextHelper import AudioToTextHelper
from Audiobook import Audiobook
import logging

def main():
    audiobook_title = 'The Animal Farm'
    youtube_url = 'https://www.youtube.com/watch?v=iosHzNmVYbA'
    audiobook = Audiobook(audiobook_title, youtube_url)

    # 1 - Download from Youtube
    youtube = YoutubeVideoHandler(audiobook)
    youtube.download()

    # 2 - Speech to Text
    audio_to_text = AudioToTextHelper(audiobook)
    audio_to_text.audio_to_text()
    audio_to_text.save_text_to_file()

    # 3 - Chapter Finder
    audiobook.find_chapters()
    print(audiobook.youtube_comment)
    return

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()