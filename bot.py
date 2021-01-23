import os
from src.handlers import *
from src.frontend import generate_access_token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, JobQueue

# Dev and logging modules
import logging
from decouple import config
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def main():
    generate_access_token()
    env = os.environ.get('ENV', 'develop')
    NAME = os.environ.get('APP_URL', "antenna-trelegram")
    TOKEN = os.environ.get('API_KEY', config('API_KEY'))
    PORT = int(os.environ.get('PORT', '8443'))

    updater = Updater(TOKEN)
    # job_queue = updater.job_queue
    dispatcher = updater.dispatcher

    # job_queue.run_daily(callback_img, time=time(21, 30, 30))
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('info', about))
    dispatcher.add_handler(CommandHandler('imagine', callback_img))
    dispatcher.add_handler(MessageHandler(Filters.text, msg_handler))
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

if __name__ == "__main__":
    main()