import telegram
from telegram.ext import Updater

ftoken = open("./token.txt", "r")
API_KEY = ftoken.read()
ftoken.close()

updater = Updater(API_KEY)
dispatcher = updater.dispatcher