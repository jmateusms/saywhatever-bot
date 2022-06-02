# Say Whatever bot

_Note that this bot is a WIP. It currently has very basic functionality and I'm not sure what will be added in the future._

Say Whatever bot is a Telegram bot that reads your messages aloud and sends them as audio. An instance of this bot is currently running. To use it, interact with the bot [@SayWhateverBot](https://t.me/SayWhateverBot) in Telegram. This instance might not be available at all times and is subject to errors, since this is still a WIP.

## Set up your own instance

### Environment variables

You can run an instance of the bot by getting a token using [Telegram's Botfather](https://telegram.me/botfather). Then add the token as an environment variable `TOKEN` (i.e., create an .env file with `TOKEN=x`, where `x` is your token).

You also need an `OWNER_ID` environment variable, which is the ID of the user who will be able to use the bot. To get your ID, run the file `get_id.py` and send `/userid` to the bot.

Lastly, you need a `DUMP_ID` variable, which is a chat ID for a group where the bot will send the generated voice recording, before sending it to the user. This must be done because Telegram's API for inline results only allows sending either a URL or a file ID. The voice recordings are sent to the `DUMP_ID` chat and then immediately deleted.

- Create a group and add the bot.
- Run the file `get_id.py` and send `/chatid` to the bot.
- Set `DUMP_ID` to the value of the chat ID.
- (Optional) Archive the chat, so that its notifications won't appear for you.

### Dependencies

Install the needed packages with:

```bash
pip install -r requirements.txt
```

### Running the bot

Run the bot with:

```bash
python saywhatever-bot.py
```

## Usage

Currently there are two ways you can use the bot:

- Write "@SayWhateverBot" in any chat and type your message after it.
- Send messages directly to the bot, starting with a language selection command (e.g., `/enus` (em-us) or `/ptbr` (pt-br)).

You can also run your own instance of the bot by following the steps in the next section.

The bot uses [gTTS](https://gtts.readthedocs.io/en/latest/index.html) for generating audio from text. gTTS is a Python package for interfacing with the Google Translate's text-to-speech API.

## Commands

Use `/help` to get a list of commands. Basic commands are:

```plaintext
/start - set language preferences
/help - get a list of commands
/tts - speak in the preferred language
```

The language options are given below:

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
