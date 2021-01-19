import os
import random
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater,\
                         CommandHandler,\
                         MessageHandler,\
                         Filters,\
                         InlineQueryHandler

# Logging module
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

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

ftoken = open("./token.txt", "r")
API_KEY = ftoken.read()
ftoken.close()

updater = Updater(API_KEY)
dispatcher = updater.dispatcher

# def start(update, context):
#     context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def zaia(update, context):
    if 'zaia' in update.message.text:
        quote=random.choice(quotes)
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

# def caps(update, context):
#     text_caps = ' '.join(context.args).upper()
#     context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

# def inline_caps(update, context):
#     query = update.inline_query.query
#     if not query:
#         return
#     results = list()
#     results.append(
#         InlineQueryResultArticle(
#             id=query.upper(),
#             title='Caps',
#             input_message_content=InputTextMessageContent(query.upper())
#         )
#     )
#     context.bot.answer_inline_query(update.inline_query.id, results)


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


# start_handler = CommandHandler('start', start)
# caps_handler = CommandHandler('caps', caps)
# echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
# inline_caps_handler = InlineQueryHandler(inline_caps)
zaia_handler = MessageHandler(Filters.text, zaia)
unknown_handler = MessageHandler(Filters.command, unknown)

# dispatcher.add_handler(start_handler)
# dispatcher.add_handler(caps_handler)
# dispatcher.add_handler(echo_handler)
# dispatcher.add_handler(inline_caps_handler)
dispatcher.add_handler(zaia_handler)
dispatcher.add_handler(unknown_handler)

updater.start_polling()
updater.idle()