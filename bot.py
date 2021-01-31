import os
from src.handlers import *
from src.frontend import generate_access_token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Dev and logging modules
import logging
from decouple import config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def main():
    generate_access_token()
    ENV = os.environ.get('ENV', 'develop')
    NAME = os.environ.get('NAME', config('NAME'))
    TOKEN = os.environ.get('API_KEY', config('API_KEY'))
    PORT = int(os.environ.get('PORT', '8443'))

    updater = Updater(TOKEN)
    queue = updater.job_queue
    dispatcher = updater.dispatcher

    queue.run_daily(daily_image, time=SEND_TIME)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('segui', subscribe))
    dispatcher.add_handler(CommandHandler('ferma', unsubscribe))
    dispatcher.add_handler(CommandHandler('info', about))
    dispatcher.add_handler(MessageHandler(Filters.update.message & (~Filters.update.edited_message), msg_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)
    

    # if ENV == 'production':
    #     updater.start_webhook(listen="0.0.0.0",
    #                         port=PORT,
    #                         url_path=TOKEN)
    #     updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
    # elif ENV == 'develop':
    #     updater.start_polling()

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()