import io
import os
import random
import logging
from datetime import date
from src.frontend import get_image
from src.graphics import process_image
from src.config import REF_DATE, Daily, Polling, QUOTES, retrieve_sheet

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded stuff, definitely to improve
# with io.open('./assets/quotes.txt', 'r', encoding='utf8') as fquotes:
#     quotes = fquotes.read().split('\n')
# fquotes.close()

# Utilities
def get_chat_info(update):
    chat_id = update.effective_chat.id
    chat_type = update.effective_chat.type
    if update.effective_chat.type == 'private':
        chat_name = update.effective_chat.username 
    elif chat_type == 'group' or chat_type == 'supergroup':
        chat_name = update.effective_chat.title 
    else:
        chat_name = 'error'
    return chat_id, chat_name

# Commands and handlers definitions
def start(update, context):
    chat_id, chat_name = get_chat_info(update)
    print(f'{chat_name} is a {update.effective_chat.type} and started the bot')
    # r.set(chat_name, chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Arei qua i fioi')

def subscribe(update, context):
    chat_id, chat_name = get_chat_info(update)
    print(f'{chat_name} is a {update.effective_chat.type} and wants to subscribe')
    # if r.exists(chat_name):
    #     context.bot.send_message(chat_id=update.effective_chat.id, text='Tranquio vecio, te sì zà a posto.')
    #     print(f'{chat_name} had already subscribed')
    # else:
    #     r.set(chat_name, chat_id)
    #     context.bot.send_message(chat_id=update.effective_chat.id, text='Bravo tosat, apuntamento ałe 8:30.')
    #     print(f'{chat_name} subscribed')

def unsubscribe(update, context):
    chat_name = get_chat_info(update)[1]
    print(f'{chat_name} is a {update.effective_chat.type} and wants to unsubscribe')
    # if r.exists(chat_name):
    #     r.delete(chat_name)
    #     context.bot.send_message(chat_id=update.effective_chat.id, text='No va mio ben sta roba, satu? Te convien strucar /segui.')
    #     print(f'{chat_name} unsubscribed')
    # else:
    #     context.bot.send_message(chat_id=update.effective_chat.id, text='Varda che te te iera zà cavà via, davero votu eser cussì sicuro de no vedar ła foto?')
    #     print(f'{chat_name} had already unsubscribed')

def msg_handler(update, context):
    quote_trig(update, context)
    wait_trig(update, context)

def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='El bot uficiałe de quei che ghe piaxe el Doxe del Veneto.')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No go mia capio.")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

# Jobs definition
def daily_image(context):
    img_path = get_image()
    days = (date.today() - REF_DATE).days
    process_image(img_path, str(days))
    # db_keys = r.keys(pattern="*")
    # for keys in db_keys:
    #     keys_values = r.get(keys).decode("UTF-8")
    #     print(f'Sending to {keys}: {keys_values}')
    #     try:
    #         context.bot.send_photo(chat_id=keys_values, photo=open(img_path, 'rb'))
    #     except Exception as ex:
    #         print(ex)
    os.unlink(img_path)

# Message Handlers definition
def quote_trig(update, context):
    if 'zaia' in update.message.text.lower():
        polling = retrieve_sheet(Polling)
        quote = ''
        dim = len(polling.get_all_records())
        quote += polling.cell(random.randint(0, dim)+1, QUOTES).value
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

        

def wait_trig(update, context):
    triggers = ['autonomi', 'venet', 'referendum', 'vot']
    for trigger in triggers:
        if trigger in update.message.text.lower():
            days = (date.today() - REF_DATE).days
            text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)