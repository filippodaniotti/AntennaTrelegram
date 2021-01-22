import io
import os
import random
import logging
from src.graphics import process_image
from datetime import date, time, timezone
from dateutil import tz 
from decouple import config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded stuff, definitely to improve
with io.open('./assets/quotes.txt', 'r', encoding='utf8') as fquotes:
    quotes = fquotes.read().split('\n')
fquotes.close()

help_message = 'El bot uficiałe de quei che ghe piaxe el Doxe del Veneto'
ref_date = date(2017, 10, 22)
send_time = time(7, 30, 0) # should be 8:30 but timezones suck

# Message Handlers definition
def zaia(update, context):
    if 'zaia' in update.message.text:
        quote=random.choice(quotes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

def wait_trig(update, context):
    triggers = ['autonomi', 'venet', 'referendum']
    for trigger in triggers:
        if trigger in update.message.text:
            days = (date.today() - ref_date).days
            text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

# Functions, commands, handler definitions
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)
    # context.job_queue.run_daily(callback_img, time=time(21, 44, 30), context=update.message.chat_id)

def msg_handler(update, context):
    zaia(update, context)
    wait_trig(update, context)

def wait_comm(update, context):
    days = (date.today() - ref_date).days
    text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)

def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No go mia capio")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

def callback_alarm(context):
    context.bot.send_message(chat_id=context.job.context, text='BEEP')

def callback_img(context):
    days = (date.today() - ref_date).days
    process_image("./assets/zaia17.jpg", str(days))
    context.bot.send_photo(chat_id=context.job.context, photo=open('./assets/zaia17.jpg', 'rb'))
    os.unlink('./assets/zaia17.jpg')


def callback_timer(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text='Setting a timer for 1 minute!')
    context.job_queue.run_daily(callback_img, time=time(21, 18, 30), context=update.message.chat_id)