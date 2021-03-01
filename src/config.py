import os
import io
import redis
import gspread
from decouple import config
from datetime import date, time
from oauth2client.service_account import ServiceAccountCredentials

### CONSTANTS ###

## Bot data
TOKEN = os.environ.get('API_KEY', config('API_KEY'))

## Date and schedule constants
REF_DATE = date(2017, 10, 22)
SEND_TIME = time(7, 30, 0) # should be 8:30 but timezones suck

## Graphic processing constants
IMG_PATH = './assets/pic.jpg'
RESOLUTION_SIZE = (960, 540)
ASPECT_RATIO = float(16/9)

DIGIT_OFFSET_W = (333, 362)
DIGIT_OFFSET_H = (456, 500)

## API call
ACCESS_TOKEN = ''
ALBUM_HASH = os.environ.get('ALBUM_HASH', config('ALBUM_HASH'))

## Heroku redis db
r = redis.from_url(os.environ.get("REDIS_URL"))

## Gdrive API credentials path
SHEET_ID = os.environ.get('SHEET_ID', config('SHEET_ID'))
CREDS = './creds.json'
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

### SHEETS COLUMNS ###

## Sheets
Daily = 0
Polling = 1

## Daily
BUONGIORNO = 1
SANTO = 2
PROVERBIO = 3

## Polling
QUOTES = 1

### UTILITIES ###

## Create Google Drive credentials
def retrieve_sheet(sheet):
    credentials = ServiceAccountCredentials.from_json_keyfile_name('./creds.json', scope)
    client = gspread.authorize(credentials)
    worksheet = client.open_by_key(SHEET_ID)
    if sheet == Daily:
        return worksheet.get_worksheet(Daily)
    elif sheet == Polling:
        return worksheet.get_worksheet(Polling)
    else:
        return worksheet.get_worksheet(Polling)

def create_gdrive_creds():
    try:
        creds = '{'
        creds += f'"type": "{os.environ.get("_type", config("_type"))}",'
        creds += f'"project_id": "{os.environ.get("project_id", config("project_id"))}",'
        creds += f'"private_key_id": "{os.environ.get("private_key_id", config("private_key_id"))}",'
        creds += f'"private_key": "{os.environ.get("private_key", config("private_key"))}",'
        creds += f'"client_email": "{os.environ.get("client_email", config("client_email"))}",'
        creds += f'"client_id": "{os.environ.get("client_id", config("client_id"))}",'
        creds += f'"auth_uri": "{os.environ.get("auth_uri", config("auth_uri"))}",'
        creds += f'"token_uri": "{os.environ.get("token_uri", config("token_uri"))}",'
        creds += f'"auth_provider_x509_cert_url": "{os.environ.get("auth_provider_x509_cert_url", config("auth_provider_x509_cert_url"))}",'
        creds += f'"client_x509_cert_url": "{os.environ.get("client_x509_cert_url", config("client_x509_cert_url"))}"'
        creds += '}'
        
        with io.open(CREDS, 'w') as json:
            json.write(creds)
    except Exception as ex:
        print(ex)
