# Antenna Trelegram
Antenna Trelegram is a [Telegram bot](https://core.telegram.org/bots/api) that sends one picture to a mailing list of Telegram chats.

## How it works
Each day at 8:30 am a job is triggered and the bot randomly retrieves an image from a private album on [Imgur](https://imgur.com/). This image is then processed by summing to it an overlay with a dinamically generated number, which is the number of days between the current date and 22/10/2017.

## How to build
If you want to test it locally you have to make sure you have an account on [Imgur](https://imgur.com/) with an album of any kind; you also have to register and authorize the application for your account, since Imgur uses OAuth2 (more info [here](https://apidocs.imgur.com/)).

You will also need [Python](https://www.python.org/) installed (of course); then, follow these steps:
* get the API key for your bot from the [BotFather](https://t.me/BotFather)
* create a local environments with all the required variables (check the [sample provided](./.env.sample))
* create the Python Virtualenv with `py -m venv env` or any name you like
* install the dependencies with `pip install -r requirements.txt` (if it doesn't work try with `pip3 install -r requirements.txt`)
* run with `python bot.py`


## Disclaimer
> This bot does make use of irony and was developed primarely for lighthearted humor of a private chat. No personal injury was inteded or even taken into account.

## Tech Stack
* [Python Telegram Bot](https://python-telegram-bot.org/) as wrapper for the Telegram API
* [OpenCV Python](https://pypi.org/project/opencv-python/) for the image processing
* [Imgur](https://imgur.com/) and the [Imgur API](https://apidocs.imgur.com/) as cloud storage for the images
* [Heroku](https://www.heroku.com) as deployment and hosting platform 
* [Heroku Redis](https://www.heroku.com/redis) as database for the mailing list