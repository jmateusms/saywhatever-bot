# Say Whatever bot

_Note that this bot is a WIP. It currently has very basic functionality and I'm not sure what will be added in the future._

Say Whatever bot is a Telegram bot that reads your messages aloud and sends them as audio. An instance of this bot is currently running. To use it, interact with the bot [@SayWhatever_bot](https://t.me/SayWhatever_bot) in Telegram. Currently you can send messages directly to the bot, starting with a language selection command (e.g., `/enus` (em-us) or `/ptbr` (pt-br)). This instance might not be available at all times and is subject to errors, since this is still a WIP.

You can also run your own instance of the bot by following the steps in the next section.

The bot uses [gTTS](https://gtts.readthedocs.io/en/latest/index.html) for generating audio from text. gTTS is a Python package for interfacing with the Google Translate's text-to-speech API.

## Set up your own instance

You can run an instance of the bot by getting a token using [Telegram's Botfather](https://telegram.me/botfather). Then add the token as an environment variable `TOKEN` (i.e., create an .env file with `TOKEN=x`, where `x` is your token).

Install the needed packages with:

```bash
pip install -r requirements.txt
```

Then, run the bot with:

```bash
python saywhatever-bot.py
```

## Command list

Use `/start` or `/help` to get a list of commands. The language options are given below:

```plaintext
/enus - speak in English (US)
/enuk - speak in English (UK)
/enau - speak in English (Australia)
/enca - speak in English (Canada)
/ennz - speak in English (New Zealand)
/enie - speak in English (Ireland)
/ensa - speak in English (South Africa)
/enin - speak in English (India)
/esmx - speak in Spanish (Mexico)
/eses - speak in Spanish (Spain)
/ptbr - speak in Portuguese (Brazil)
/ptpt - speak in Portuguese (Portugal)
/frfr - speak in French (France)
/frca - speak in French (Canada)
```
