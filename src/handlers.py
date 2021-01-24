import io
import os
import redis
import random
import logging
from datetime import date, time
from src.frontend import get_image
from src.graphics import process_image
# from decouple import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

REF_DATE = date(2017, 10, 22)
SEND_TIME = time(7, 30, 0) # should be 8:30 but timezones suck
help_message = 'El bot uficiałe de quei che ghe piaxe el Doxe del Veneto'

r = redis.from_url(os.environ.get("REDIS_URL"))

# Hardcoded stuff, definitely to improve
with io.open('./assets/quotes.txt', 'r', encoding='utf8') as fquotes:
    quotes = fquotes.read().split('\n')
fquotes.close()

# Functions, commands, handler definitions
def start(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    r.set(user_name, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Arei qua i fioiii')
    # context.job_queue.run_daily(callback_img, time=SEND_TIME)

def subscribe(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.from_user.name
    pass

def unsubscribe(context, update):
    pass

def msg_handler(update, context):
    quote_trig(update, context)
    wait_trig(update, context)

def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No go mia capio")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def test(update, context):
    db_keys = r.keys(pattern="*")
    for keys in db_keys:
        keys_values = r.get(keys).decode("UTF-8")
        print(keys_values)
        context.bot.send_message(chat_id=keys_values, text='pls funzia')

# def wait(update, context):
#     days = (date.today() - ref_date).days
#     text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text)


# Jobs definition
def daily_image(context):
    img_path = get_image()
    days = (date.today() - REF_DATE).days
    process_image(img_path, str(days))
    db_keys = r.keys(pattern="*")
    for keys in db_keys:
        keys_values = r.get(keys).decode("UTF-8")
        print(keys_values)
        context.bot.send_photo(chat_id=keys_values, photo=open(img_path, 'rb'))
    # context.bot.send_photo(chat_id=context.job.context, photo=open(img_path, 'rb'))
    # context.bot.send_photo(chat_id=, photo=open(img_path, 'rb'))
    os.unlink(img_path)

# Message Handlers definition
def quote_trig(update, context):
    if 'zaia' in update.message.text:
        quote=random.choice(quotes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

def wait_trig(update, context):
    triggers = ['autonomi', 'venet', 'referendum', 'vot']
    for trigger in triggers:
        if trigger in update.message.text:
            days = (date.today() - REF_DATE).days
            text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)