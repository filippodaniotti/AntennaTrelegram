from src.config import TOKEN, SEND_TIME, create_gdrive_creds
from src.handlers import *
from src.frontend import generate_access_token
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# logging modules
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

def main():
    # Main app setup
    generate_access_token()
    create_gdrive_creds()

    updater = Updater(TOKEN)
    queue = updater.job_queue
    dispatcher = updater.dispatcher

    # Adding handlers
    queue.run_daily(daily_image, time=SEND_TIME)
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('segui', subscribe))
    dispatcher.add_handler(CommandHandler('ferma', unsubscribe))
    dispatcher.add_handler(CommandHandler('info', about))
    # dispatcher.add_handler(CommandHandler('im', im))
    dispatcher.add_handler(MessageHandler(Filters.update.message & (~Filters.update.edited_message), msg_handler))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()