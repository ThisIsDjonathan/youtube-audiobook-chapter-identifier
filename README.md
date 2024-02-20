
<h1 align="center">Welcome to youtube-audiobook-chapter-identifier 🎧📖 </h1>

This project goal is to identify the chapters in an audiobook hosted on YouTube 🔎🕵🏻‍♂️📋

# Example
```
Capítulo 1 	 0:15:09
Capítulo 2 	 0:24:50
Capítulo 3 	 0:33:07
Capítulo 4 	 0:45:47
Capítulo 5 	 0:52:30
```

# How I built this
This is done in 3 steps:
1. The `YoutubeVideoHandler.py` will download the YouTube content as a `.mp4`;
2. Then the `AudioToTextHandler.py` will use the [OpenAI whisper](https://github.com/openai/whisper) to transcribe the audio to text;
3. The last step is done by the `ChaperFinder.py` which will find where each chapter starts based on the result text from the step above.

## YoutubeVideoHandler
We are using the [pytube](https://github.com/pytube/pytube) library to download the Youtube data. 
```
youtube = YoutubeVideoHandler('https://www.youtube.com/watch?v=iosHzNmVYbA')
youtube.download()
```

The `download()` function will create a new directory for the audiobook we're downloading


📦 youtube-audiobook-chapter-identifier<br>
┣ 📂 data<br>
┃ ┗ 📂 George Orwell - Animal Farm<br>
┃   ┗ 📂 youtube-data <br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `George Orwell - Animal Farm.mp4`<br>
┃   ┗ 📂 audio-to-text <br>
┃&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┗ 🎧 `366.mp3`<br>

## The Speech to Text 🗣️👂✍🏻
The Alexa Skill is a Flash Briefing skill created in the [Alexa Developer Console](https://developer.amazon.com/alexa/console) that will consume our JSON feed API hosted on AWS.
<br>These are the docs I used for reference:<br>
- [Understand the Flash Briefing Skill](https://developer.amazon.com/en-US/docs/alexa/flashbriefing/understand-the-flash-briefing-skill-api.html)
- [Flash Briefing Skill API Feed Reference](https://developer.amazon.com/en-US/docs/alexa/flashbriefing/flash-briefing-skill-api-feed-reference.html)


## Contributing 🤝
### You can contribute by adding support for more languages! 🌎<br>

#### Running the code
Then let's run the code in your environment!
First, install the Python dependencies `python-dotenv` and `elevenlabs`:
```sh
pip install -r requirements.txt
```

Then update the `.env` file by adding your API Key.
📦 daily-stoic-alexa-skill
┣ 📜 `.env`
```
API_KEY='your API key goes here'
```

Update the `main()` function in the `text-to-speech.py` file adding your language the run `python text-to-speech.py`:
```
def main():
    language = 'portuguese'
    create_folders_if_not_exists(language)

    quotes = get_quotes_from_file('./assets/quotes/quotes-in-' + language + '.json')
    process_data(quotes, language)

    # add your code here!
    language = 'your language' # TODO: add your language here
    create_folders_if_not_exists(language)

    quotes = get_quotes_from_file('./assets/quotes/quotes-in-' + language + '.json')
    process_data(quotes, language)
```

#### Push a PR
Finally, push a PR to this repo. I will merge it, add the new audio files to the S3 bucket, and make the Alexa Skill available in your country.
Please specify the language you are adding, the country where you are from, and your name to the PR description!

## Author
👤 **Djonathan Krause**
- Website: [djonathan.com](https://www.djonathan.com)
- Github: [@ThisIsDjonathan](https://github.com/ThisIsDjonathan)

## Show your support
Please ⭐️ this repository if this project helped you!
<br><br><a href="https://www.buymeacoffee.com/djonathan" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a>

