# import packages
import os
from dotenv import load_dotenv
import telebot
from telebot import types
from gtts import gTTS
from io import BytesIO
import requests
from utils import *

# load api token and owner id
load_dotenv()
TOKEN = os.getenv('TOKEN')

def get_audio(text, lang='en', tld='com'):
    tts = gTTS(text=text, lang=lang, tld=tld)
    fp = BytesIO()
    tts.write_to_fp(fp)
    fp.seek(0)
    return fp
    # fname = f'audio_{lang}_{tld}.mp3'
    # tts.save(fname)
    # return fname

# create bot
bot = telebot.TeleBot(TOKEN)

# start bot memory
mem = memo()

@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.send_message(message.chat.id,
    '''
Hi, I'm Say Whatever bot! Send me a message starting with one of the commands for language/accent selection and I will read them aloud.

If you set your preferred language/accent (with /setup), you will be able to use me directly in other chats, by starting your message with @SayWhatever_bot. This also allows you to use the /tts command, which will use your preferred settings.

/start, /help - show this message
/setup - set up your preferences
/tts - speak in your preferred language
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
''')

@bot.message_handler(commands=['setup'])
def setup(message):
    if message.chat.id in mem.user_prefs:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Yes', 'No')
        bot.send_message(message.chat.id, f'Your preferred language/accent is already set to {mem.user_prefs[message.chat.id]["name"]}. Do you want to change it?', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('English (US)', 'English (UK)', 'English (Australia)', 'English (Canada)', 'English (New Zealand)', 'English (Ireland)', 'English (South Africa)', 'English (India)', 'Spanish (Mexico)', 'Spanish (Spain)', 'Portuguese (Brazil)', 'Portuguese (Portugal)', 'French (France)', 'French (Canada)')
        bot.send_message(message.chat.id, 'Please select your preferred language/accent:', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)

@bot.message_handler(commands=[])
def setup_lang(message):
    if message.text == 'English (US)':
        lang = 'en'
        tld = 'com'
    elif message.text == 'English (UK)':
        lang = 'en'
        tld = 'co.uk'
    elif message.text == 'English (Australia)':
        lang = 'en'
        tld = 'com.au'
    elif message.text == 'English (Canada)':
        lang = 'en'
        tld = 'ca'
    elif message.text == 'English (New Zealand)':
        lang = 'en'
        tld = 'co.nz'
    elif message.text == 'English (Ireland)':
        lang = 'en'
        tld = 'ie'
    elif message.text == 'English (South Africa)':
        lang = 'en'
        tld = 'co.za'
    elif message.text == 'English (India)':
        lang = 'en'
        tld = 'in'
    elif message.text == 'Spanish (Mexico)':
        lang = 'es'
        tld = 'com.mx'
    elif message.text == 'Spanish (Spain)':
        lang = 'es'
        tld = 'es'
    elif message.text == 'Portuguese (Brazil)':
        lang = 'pt'
        tld = 'com.br'
    elif message.text == 'Portuguese (Portugal)':
        lang = 'pt'
        tld = 'pt'
    elif message.text == 'French (France)':
        lang = 'fr'
        tld = 'fr'
    elif message.text == 'French (Canada)':
        lang = 'fr'
        tld = 'ca'
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('English (US)', 'English (UK)', 'English (Australia)', 'English (Canada)', 'English (New Zealand)', 'English (Ireland)', 'English (South Africa)', 'English (India)', 'Spanish (Mexico)', 'Spanish (Spain)', 'Portuguese (Brazil)', 'Portuguese (Portugal)', 'French (France)', 'French (Canada)')
        bot.send_message(message.chat.id, 'Please select your preferred language/accent:', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)
        return
    mem.user_prefs[message.chat.id] = {'name': message.text, 'lang': lang, 'tld': tld}
    bot.send_message(message.chat.id, f'Your preferred language/accent has been set to {mem.user_prefs[message.chat.id]["name"]}.')

@bot.message_handler(commands=['tts'])
def tts(message):
    if len(message.text) < 5:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    elif message.chat.id in mem.user_prefs:
        text = message.text[4:]
        try:
            fp = get_audio(
                text,
                lang=mem.user_prefs[message.chat.id]['lang'],
                tld=mem.user_prefs[message.chat.id]['tld'])
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')
            return
        bot.send_voice(message.chat.id, voice=fp)
    else:
        bot.send_message(message.chat.id, 'Please set your preferred language/accent with /setup.')

@bot.message_handler(commands=['enus'])
def enus(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='com'))
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enuk'])
def enuk(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='co.uk'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enau'])
def enau(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='com.au'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enca'])
def enca(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='ca'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ennz'])
def ennz(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='co.nz'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enie'])
def enie(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='ie'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ensa'])
def ensa(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='co.za'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enin'])
def enin(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='en', tld='co.in'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['esmx'])
def esmx(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='es', tld='com.mx'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['eses'])
def eses(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='es', tld='es'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ptbr'])
def ptbr(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='pt', tld='com.br'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ptpt'])
def ptpt(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='pt', tld='pt'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['frfr'])
def frfr(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='fr', tld='fr'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['frca'])
def frca(message):
    if len(message.text) < 7:
        bot.send_message(message.chat.id, 'The text must not be empty.')
    else:
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(message.text[6:], lang='fr', tld='ca'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

if __name__ == '__main__':
    while True:
        try:
            bot.polling(non_stop=True)
            # yes, this is ugly, but it crashes sometimes otherwise due to
            # random timeouts
        except telebot.apihelper.ApiTelegramException as e:
            print(e)
        except requests.exceptions.ConnectionError as e:
            print(e)
        except requests.exceptions.ReadTimeout as e:
            print(e)

