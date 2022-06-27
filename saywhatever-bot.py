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
OWNER_ID = int(os.getenv('OWNER_ID'))
DUMP_ID = int(os.getenv('DUMP_ID'))

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

@bot.message_handler(commands=['help'])
def start(message):
    bot.send_message(message.chat.id,
    '''
Hi, I'm SayWhatever bot! Send me a message starting with one of the commands for language/accent selection and I will read them aloud.

If you set your preferred language/accent (with /setup), you will be able to use me directly in other chats, by starting your message with @SayWhateverBot. This also allows you to use the /tts command, which will use your preferred settings.

/start - set up your preferences
/help - show this message
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

@bot.message_handler(commands=['reset'])
def reset(message):
    if message.from_user.id in [OWNER_ID]:
        mem.create_mem()
        bot.send_message(message.chat.id, 'Memory reset')
    else:
        bot.send_message(message.chat.id, f'You are not my owner.')
        print(type(OWNER_ID))
        print(OWNER_ID)
        print(type(message.from_user.id))
        print(message.from_user.id)
        print(type(message.chat.id))
        print(message.chat.id)

@bot.message_handler(commands=['start'])
def setup(message):
    if message.from_user.id in mem.user_prefs:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Yes', 'No')
        bot.send_message(message.chat.id, f'Your preferred language/accent is already set to {mem.user_prefs[message.from_user.id]["name"]}. Do you want to change it?', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)
    else:
        bot.send_message(message.chat.id, "Hi, I'm SayWhatever bot! Let's set up your preferences for using the bot.")
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('English (US)', 'English (UK)', 'English (Australia)', 'English (Canada)', 'English (New Zealand)', 'English (Ireland)', 'English (South Africa)', 'English (India)', 'Spanish (Mexico)', 'Spanish (Spain)', 'Portuguese (Brazil)', 'Portuguese (Portugal)', 'French (France)', 'French (Canada)')
        bot.send_message(message.chat.id, 'Please select your preferred language/accent:', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)

@bot.message_handler(commands=[])
def setup_lang(message):
    if message.text == 'No':
        return
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
    elif message.text == 'Yes':
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('English (US)', 'English (UK)', 'English (Australia)', 'English (Canada)', 'English (New Zealand)', 'English (Ireland)', 'English (South Africa)', 'English (India)', 'Spanish (Mexico)', 'Spanish (Spain)', 'Portuguese (Brazil)', 'Portuguese (Portugal)', 'French (France)', 'French (Canada)')
        bot.send_message(message.chat.id, 'Please select your preferred language/accent:', reply_markup=markup)
        bot.register_next_step_handler(message, setup_lang)
        return
    else:
        markup = types.ReplyKeyboardRemove(selective=False)
        bot.send_message(message.chat.id, 'No changes made to your preferred language/accent.', reply_markup=markup)
        return
    mem.user_prefs[message.from_user.id] = {'name': message.text, 'lang': lang, 'tld': tld}
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, f'Your preferred language/accent has been set to {mem.user_prefs[message.from_user.id]["name"]}.\nYou can use me in other chats by starting your message with @SayWhateverBot, or send me a private message starting with /tts. For a full list of commands, type /help.', reply_markup=markup)
    mem.sync_mem()

@bot.message_handler(commands=['tts'])
def tts(message, ignore_size=False):
    if len(message.text) < 5 and not ignore_size:
        # bot.send_message(message.chat.id, 'The text must not be empty.')
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, tts, True)
        return
    elif message.from_user.id in mem.user_prefs:
        if ignore_size:
            text = message.text
        else:
            text = message.text[4:]
        try:
            fp = get_audio(
                text,
                lang=mem.user_prefs[message.from_user.id]['lang'],
                tld=mem.user_prefs[message.from_user.id]['tld'])
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')
            return
        bot.send_voice(message.chat.id, voice=fp)
    else:
        bot.send_message(message.chat.id, 'Please set your preferred language/accent with /setup.')

@bot.inline_handler(lambda query: type(query.query) == str)
def inline_query(query):
    if not query.from_user.id in mem.user_prefs:
        bot.answer_inline_query(query.id, [], switch_pm_text='Set your preferred language/accent.', switch_pm_parameter='setup', cache_time=0)
        return
    try:
        fp = get_audio(
            query.query,
            lang=mem.user_prefs[query.from_user.id]['lang'],
            tld=mem.user_prefs[query.from_user.id]['tld'])
        fp_voice = bot.send_voice(DUMP_ID, voice=fp, disable_notification=True)
        fp_id = fp_voice.voice.file_id
        bot.answer_inline_query(
            query.id, [types.InlineQueryResultCachedVoice(
                id=query.query,
                voice_file_id=fp_id,
                title=f'Spoken text in {mem.user_prefs[query.from_user.id]["name"]}.')], cache_time=0)
        bot.delete_message(DUMP_ID, fp_voice.message_id)
    except AssertionError:
        pass

@bot.message_handler(commands=['enus'])
def enus(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enus, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='com'))
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enuk'])
def enuk(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enuk, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='co.uk'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enau'])
def enau(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enau, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='com.au'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enca'])
def enca(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enca, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='ca'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ennz'])
def ennz(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, ennz, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='co.nz'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enie'])
def enie(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enie, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='ie'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ensa'])
def ensa(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, ensa, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='co.za'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['enin'])
def enin(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, enin, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='en', tld='co.in'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['esmx'])
def esmx(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, esmx, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='es', tld='com.mx'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['eses'])
def eses(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, eses, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='es', tld='es'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ptbr'])
def ptbr(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, ptbr, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='pt', tld='com.br'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['ptpt'])
def ptpt(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, ptpt, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='pt', tld='pt'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['frfr'])
def frfr(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, frfr, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='fr', tld='fr'),
            )
        except AssertionError:
            bot.send_message(message.chat.id, 'Your text could not be spoken.')

@bot.message_handler(commands=['frca'])
def frca(message, ignore_size=False):
    if len(message.text) < 7 and not ignore_size:
        markup = telebot.types.ForceReply(selective=False)
        get_reply = bot.send_message(message.chat.id, "Please, type a message:", reply_markup=markup)
        bot.register_next_step_handler(get_reply, frca, True)
        return
    else:
        if ignore_size:
            text = message.text
        else:
            text = message.text[6:]
        try:
            bot.send_voice(
                message.chat.id,
                get_audio(text, lang='fr', tld='ca'),
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

