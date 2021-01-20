import os
import random
# from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Dev modules
from decouple import config

# Logging module
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

# Hardcoded quotes just to try it our
quotes = [
    "Il Veneto con le sue scelte di condivisione e non di coercizione, è più favorevole ai vaccini di tante altre Regioni perché l'informazione e la condivisione aumentano le adesioni, l'obbligatorietà le farà calare",
    "Io penso che la Cina abbia pagato un grande conto di questa epidemia che ha avuto, perché comunque li abbiamo visti tutti mangiare i topi vivi o altre robe del genere",
    "Per i cristiani è il segno del loro credo religioso. Per i non cristiani è un segno identitario. [...] le nostre comunità sono letteralmente scolpite dalla cultura cristiana e dal cristianesimo",
    "Si tratta solo di realizzarla, ma il problema è che a Roma, ma non solo, si continua a vedere l'autonomia come una sottrazione di potere. E invece è tutt'altro: un'assunzione di responsabilità",
    "Siamo tutti figli della Serenissima, fondata sull'idea della sua autonomia",
    "Utilizzate questo palcoscenico per parlare anche di temi che magari sono più ostici come il tema dell'omofobia, e lo dico da eterosessuale convinto: mi auguro che qui si possa chiarire una volta per tutte che l'omofobia è una patologia",
    "Volere bene al Paese non significa solo cantare bene l'Inno di Mameli e sventolare il Tricolore"
]

help_message = '''
    El bot uficiałe de quei che ghe piaxe el Doxe del Veneto
'''

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def zaia(update, context):
    if 'zaia' in update.message.text:
        quote=random.choice(quotes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)
    # if 'troie' in update.message.text:
    #     context.bot.send_photo(chat_id=update.effective_chat.id, photo=open('./pr.jpg', 'rb'))

def about(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="No go mia capio")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)

if __name__ == "__main__":
    env = os.environ.get('ENV', 'develop')
    NAME = os.environ.get('APP_URL', "antenna-trelegram")
    TOKEN = os.environ.get('API_KEY', config('API_KEY'))
    PORT = int(os.environ.get('PORT', '8443'))

    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('Start', start))
    dispatcher.add_handler(CommandHandler('About', about))
    dispatcher.add_handler(MessageHandler(Filters.text, zaia))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    if env == 'production':
        updater.start_webhook(listen="0.0.0.0",
                            port=PORT,
                            url_path=TOKEN)
        updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    elif env == 'develop':
        updater.start_polling()

    updater.idle()