import io
import os
import random
import logging
from datetime import date
from src.frontend import get_image
from src.graphics import process_image
from src.config import REF_DATE, Daily, Polling, QUOTES, PROVERBIO, SANTO, BUONGIORNO, retrieve_sheet, r

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

## DECORATORS
def triggerslist(trig):
    def inner(*args, **kwargs):
        chat_name = get_chat_info(args[0])[1]
        if r.exists(chat_name):
            trig(*args, **kwargs)

    return inner

# def subscription(action):
#     def inner(*args, **kwargs):
#         chat_id, chat_name = get_chat_info(update)

#     return inner


# Utilities
def get_chat_info(update):
    chat_id = update.message.chat.id
    chat_type = update.message.chat.type
    if chat_type == 'private':
        chat_name = update.message.chat.username 
    elif chat_type == 'group' or chat_type == 'supergroup':
        chat_name = update.message.chat.title 
    else:
        chat_name = 'error'
    return chat_id, chat_name

# Commands and handlers definitions
def start(update, context):
    chat_id, chat_name = get_chat_info(update)
    print(f'{chat_name} is a {update.effective_chat.type} and started the bot')
    r.set(chat_name, chat_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text='Arei qua i fioi')

def subscribe(update, context):
    chat_id, chat_name = get_chat_info(update)
    print(f'{chat_name} is a {update.effective_chat.type} and wants to subscribe')
    if r.exists(chat_name):
        context.bot.send_message(chat_id=update.effective_chat.id, text='Tranquio vecio, te sì zà a posto.')
        print(f'{chat_name} had already subscribed')
    else:
        r.set(chat_name, chat_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text='Bravo tosat, apuntamento ałe 8:30.')
        print(f'{chat_name} subscribed')

def unsubscribe(update, context):
    chat_name = get_chat_info(update)[1]
    print(f'{chat_name} is a {update.effective_chat.type} and wants to unsubscribe')
    if r.exists(chat_name):
        r.delete(chat_name)
        context.bot.send_message(chat_id=update.effective_chat.id, text='No va mio ben sta roba, satu? Te convien strucar /segui.')
        print(f'{chat_name} unsubscribed')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='Varda che te te iera zà cavà via, davero votu eser cussì sicuro de no vedar ła foto?')
        print(f'{chat_name} had already unsubscribed')

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
    caption = compose_caption()
    db_keys = r.keys(pattern="*")
    for keys in db_keys:
        keys_values = r.get(keys).decode("UTF-8")
        print(f'Sending to {keys}: {keys_values}')
        try:
            context.bot.send_photo(chat_id=keys_values, photo=open(img_path, 'rb'), caption=caption)
        except Exception as ex:
            print(ex)
    os.unlink(img_path)

def compose_caption():
    caption = ''
    daily = retrieve_sheet(Daily)
    rows = len(daily.get_all_records()) + 1

    cells = list()
    count = 0
    while count < 3:
        new_rand = random.randint(2, rows)
        if daily.cell(new_rand, count + 1).value != None:
            cells.append(daily.cell(new_rand, count + 1).value)
            count += 1

    caption += f"AREI TOSI\n{cells[0]}\n\n"
    caption += f"El santo del giorno secondo el calendario el xe:\n{cells[1]}\n\n"
    caption += f"E me racomando, ricordeve quel che i dixe i veci:\n{cells[2]}"
    return caption

# Message Handlers definition
@triggerslist
def quote_trig(update, context):
    if 'zaia' in update.message.text.lower():
        polling = retrieve_sheet(Polling)
        quote = ''
        rows = len(polling.get_all_records()) + 1
        quote += polling.cell(random.randint(2, rows), QUOTES).value
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

        
@triggerslist
def wait_trig(update, context):
    triggers = ['autonomi', 'venet', 'referendum', 'vot']
    for trigger in triggers:
        if trigger in update.message.text.lower():
            days = (date.today() - REF_DATE).days
            text = f"Ennesimo rinvio par la autonomia, è una presa in giro: la misura è colma. Semo {str(days)} giorni in atesa del governo, can del porco!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=text)

## DEBUG

# def im(update, context):
#     img_path = get_image()
#     days = (date.today() - REF_DATE).days
#     process_image(img_path, str(days))
#     caption = compose_caption()
#     try:
#         context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img_path, 'rb'), caption=caption)
#     except Exception as ex:
#         print(ex)
#     os.unlink(img_path)