import whisper
import json
import os
from pytube import YouTube, exceptions
import logging
import datetime
import re

YOUTUBE_DATA_DIRECTORY = './assets/youtube-data/'

DIR_PATH_AUDIOS = './assets/downloaded-audios/'
DIR_TEXT_BASE_PATH = './assets/speech-to-text-result/'
RESULTS_DIR = './assets/results/'

def download_youtube_audio(url):
    try:
        logging.info("Downloading Youtube video...")
        youtube = YouTube(url)
        youtube.register_on_progress_callback(log_download_progress_function)
        audio = youtube.streams.get_audio_only()
        audio.download(DIR_PATH_AUDIOS)
        return audio.title
    except Exception as e:
        logging.error(f"An error occurred while downloading the video. ERROR: {e}")

def speech_to_text(audio_filename):
    try:
        logging.info("--------------------------------------")
        logging.info("Converting speech-to-text...")
        logging.info("--------------------------------------")

        full_file_path = os.path.join(DIR_PATH_AUDIOS, audio_filename)
        model = whisper.load_model('base')
        result = model.transcribe(full_file_path)
        return result
    except Exception as e:
        logging.error(f"An error occurred while converting audio to text. ERROR: {e}")

def save_speech_to_text_to_file(result, audiobook_title):
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    result_filename = audiobook_title + '.json'
    result_full_file_path = os.path.join(DIR_TEXT_BASE_PATH, result_filename)

    os.makedirs(DIR_TEXT_BASE_PATH, exist_ok=True)

    with open(result_full_file_path, 'w', encoding='utf-8') as file:
        file.write(result_json)

    return result_full_file_path

def get_chapters_from_result_file(result_full_file_path):
    logging.info("Searching for chapters...")
    with open(result_full_file_path, 'r') as json_file:
        result = json.load(json_file)

    segments = result['segments']
    chapters = []
    for segment in segments:
        if 'cap\u00edtulo' in segment['text'].lower() or 'capítulo' in segment['text'].lower():
            chapter_title = get_chapter_only_from_text_segment(segment['text'])
            if chapter_title is None:
                continue
            chapter = {
                'title': chapter_title,
                'start': segment['start']
            }
            chapters.append(chapter)
    return chapters

def get_chapter_only_from_text_segment(text):
    match = re.search(r'(Cap\u00edtulo \d+)', text)
    if match:
        return match.group(0)
    else:
        return None

def calc_and_set_duration_to_chapters(chapters):
    for i in range(len(chapters)):
        if i == 0:
            chapters[i]['duration'] = chapters[i]['start']
            continue
        chapters[i]['duration'] = chapters[i]['start'] - chapters[i-1]['start']
    return chapters


def save_chapters_to_json(chapters, audio_filename):
    if not os.path.exists('./results'):
        os.makedirs('./results')

    chapters_filename = audio_filename.split('.')[0] + '.json'
    chapters_filename = './results/' + chapters_filename
    logging.info(f"Saving chapters to `{chapters_filename}`")
    with open(chapters_filename, 'w') as f:
        f.write(json.dumps(chapters, indent=4))

def seconds_to_time(seconds):
    return str(datetime.timedelta(seconds=int(seconds)))

def parse_result_to_youtube_comment_format(chapters):
    logging.info("Parsing chapters to youtube comment format...")
    youtube_comment = []
    for i in range(len(chapters)):
        chapter_title = chapters[i]['title']
        chapter_start_in_seconds = chapters[i]['start']
        chapter_start_at = seconds_to_time(chapter_start_in_seconds)
        chapter_duration = seconds_to_time(chapters[i]['duration'])

        youtube_comment.append({
            'chapter_title': chapter_title,
            'chapter_start_at': chapter_start_at,
            'chapter_duration': chapter_duration
        })

    for chapter in youtube_comment:
         print(f"{chapter['chapter_title']} \t {chapter['chapter_start_at']} \t Duration: {chapter['chapter_duration']}")

def main():
    audiobook_title = download_youtube_audio('https://www.youtube.com/watch?v=0rXsO9HRgfo&t=22273s')

    #speech_to_text_result = speech_to_text(audiobook_title)
    #speech_to_text_result_file_path = save_speech_to_text_to_file(speech_to_text_result, audiobook_title)
    
    speech_to_text_result_file_path = "Dan Brown O Símbolo Perdido! parte 2 final.json"
    
    chapters = get_chapters_from_result_file(speech_to_text_result_file_path)
    chapters = calc_and_set_duration_to_chapters(chapters)

    save_chapters_to_json(chapters, audiobook_title)
    parse_result_to_youtube_comment_format(chapters)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()