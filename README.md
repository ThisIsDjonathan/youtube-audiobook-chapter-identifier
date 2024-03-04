
<h1 align="center">Welcome to youtube-audiobook-chapter-identifier 🎧📖 </h1>

This bot's goal is to identify the chapters in an audiobook hosted on YouTube 🔎🕵🏻‍♂️📋
<p align="center"><img src="https://github.com/ThisIsDjonathan/youtube-audiobook-chapter-identifier/assets/8337704/63c6927d-9fd7-4d8c-8899-23a6377b61fc" alt="bot-image" width="300"></p>

# Result Example
```
__________________
Result for The Animal Farm
https://www.youtube.com/watch?v=iosHzNmVYbA

Chapter 1        0:00:07         Duration: 0:00:07
Chapter 2        0:16:51         Duration: 0:16:43
Chapter 3        0:33:05         Duration: 0:16:14
Chapter 4        0:47:13         Duration: 0:14:07
Chapter 5        0:57:48         Duration: 0:10:34
Chapter 6        1:17:14         Duration: 0:19:26
Chapter 7        1:34:49         Duration: 0:17:35
Chapter 8        1:57:52         Duration: 0:23:03
Chapter 9        2:22:48         Duration: 0:24:55
Chapter 10       2:45:23         Duration: 0:22:34


by https://github.com/ThisIsDjonathan/youtube-audiobook-chapter-identifier
__________________
```

# How I Built This
This is done in 3 steps:
1. The `YoutubeVideoHelper.py` will download the YouTube content as a `.mp4`;
2. Then the `AudioToTextHelper.py` will use the [OpenAI whisper](https://github.com/openai/whisper) to transcribe the audio to text;
3. The last step is done by the `Audiobook.py` which will find where each chapter starts based on the result text from the step above.

The script will create a folder inside the `./audiobooks/` directory for each audiobook.

This is the file structure:
📦 youtube-audiobook-chapter-identifier<br>
┣ 📂 audiobooks<br>
┃ ┗ 📂 Audio Book 1<br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `youtube-content.mp4`<br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 📋 `audio-to-text.json`<br>

# How to use it
First, install the Python dependencies:
```sh
pip install -r requirements.txt
```

Then update the `main.py` setting the Audiobook title and its Youtube URL.
```
def main():
    audiobook_title = 'The Animal Farm'
    youtube_url = 'https://www.youtube.com/watch?v=iosHzNmVYbA'
```

And finally run the script: `python main.py`

# How it Works

## YoutubeVideoHandler 🎧📖
We are using the [pytube](https://github.com/pytube/pytube) library to download the Youtube data.
We download the audio only and save the file as `youtube-content.mp4`.

## The Speech to Text 🗣️👂✍🏻
After download the audio file from YouTube we use the [OpenAI whisper](https://github.com/openai/whisper) to transcribe the audio to text.
The result of this process is a JSON file saved as `audio-to-text.json`

## Chapter Finder 🕵🏻‍♂️📋
The chapter finder (`Audiobook.find_chapters()`) will loop through each segment resulted in the whisper transcription and look for the word "chapter". This should be done in a better way since currently I'm using a simple and dumb `if` statement to do so 😅

# Contributing
Check the open issues 😁

## Author
👤 **Djonathan Krause**
- Website: [djonathan.com](https://www.djonathan.com)
- Github: [@ThisIsDjonathan](https://github.com/ThisIsDjonathan)

## Show your support
Please ⭐️ this repository if this project helped you!
<br><br><a href="https://www.buymeacoffee.com/djonathan" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

