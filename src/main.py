import whisper
import json
import os
from pytube import YouTube, exceptions
import logging
import datetime
import re

DIR_PATH_AUDIOS = './audios/'
DIR_TEXT_BASE_PATH = './texts/'
RESULTS_DIR = './results/'
MODEL_NAME = 'base'

def transcribe_audio_to_text(audio_filename):
    import whisper  # Import here to avoid unnecessary import if function is not used
    try:
        logging.info("Converting audio to text...")
        model = whisper.load_model(MODEL_NAME)
        full_file_path = os.path.join(DIR_PATH_AUDIOS, audio_filename)
        result = model.transcribe(full_file_path)
        return result
    except Exception as e:
        logging.error(f"An error occurred while converting audio to text: {e}")

def save_transcription_result(result, audio_filename):
    result_json = json.dumps(result, indent=4, ensure_ascii=False)
    result_filename = os.path.splitext(audio_filename)[0] + '.json'
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

def set_duration_to_chapters(chapters):
    for i in range(len(chapters)):
        if i == 0:
            chapters[i]['duration'] = chapters[i]['start']
            continue
        chapters[i]['duration'] = chapters[i]['start'] - chapters[i-1]['start']
    return chapters

def download_youtube_audio(url):
    try:
        logging.info("Downloading Youtube video...")
        youtube = YouTube(url)
        youtube.register_on_progress_callback(log_download_progress_function)
        audio = youtube.streams.get_audio_only()
        default_filename = audio.default_filename
        audio.download(DIR_PATH_AUDIOS)
        return default_filename
    except exceptions.PytubeError as e:
        logging.error(f"An error occurred while downloading the video: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while download the youtube video: {e}")

def log_download_progress_function(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage_of_completion = round(bytes_downloaded / total_size * 100)
    logging.info(f"Downloaded {percentage_of_completion}% of the video")

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
    logging.basicConfig(level=logging.INFO)
    # audio_filename = download_youtube_audio('https://www.youtube.com/watch?v=EZ0cnZhPnZI&t=18188s')
    # audio_to_text_result = transcribe_audio_to_text(audio_filename)
    # audio_to_text_result_file_path = save_transcription_result(audio_to_text_result, audio_filename)

    audio_to_text_result_file_path = './texts/Dan Brown O Símbolo Perdido! parte 1.json'
    audio_filename = 'Dan Brown O Símbolo Perdido! parte 1.mp4'
    chapters = extract_chapters_from_result_file(audio_to_text_result_file_path)
    chapters = calculate_chapter_durations(chapters)
    save_chapters_to_json(chapters, audio_filename)
    print_chapters_in_youtube_comment_format(chapters)

if __name__ == "__main__":
    main()