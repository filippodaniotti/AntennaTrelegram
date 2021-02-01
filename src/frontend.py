import os
import requests
import random
from decouple import config
# from urllib.parse import urlparse

from requests.api import get

ACCESS_TOKEN = ''
ALBUM_HASH = os.environ.get('ALBUM_HASH', config('ALBUM_HASH'))
IMG_PATH = './assets/pic.jpg'

def get_image() -> str:
	print("Fetching image...")
	url = f"https://api.imgur.com/3/album/{ALBUM_HASH}/images"
	headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
	response = requests.request("GET", url, headers=headers)
	
	# if access token has expired
	if response.status_code == 403:
		generate_access_token()
		headers = {'Authorization': f'Bearer {ACCESS_TOKEN}'}
		response = requests.request("GET", url, headers=headers)

	images = response.json()['data']
	img_url = random.choice(images)['link']
	image = requests.get(img_url)
	
	print("Saving image...")
	with open(IMG_PATH, "wb") as f:
		f.write(image.content)
	print("Done")
	return IMG_PATH

def generate_access_token():
	global ACCESS_TOKEN
	print("Generating new access token")
	url = "https://api.imgur.com/oauth2/token"
	refresh_token = os.environ.get('REFRESH_TOKEN', config('REFRESH_TOKEN'))
	client_id = os.environ.get('CLIENT_ID', config('CLIENT_ID'))
	client_secret = os.environ.get('CLIENT_SECRET', config('CLIENT_SECRET'))

	payload = {'refresh_token': f'{refresh_token}',
	'client_id': f'{client_id}',
	'client_secret': f'{client_secret}',
	'grant_type': 'refresh_token'}
	files = []
	headers= {}
	response = requests.request("POST", url, headers=headers, data = payload, files = files)
	ACCESS_TOKEN = response.json()['access_token']
	print("Done")

# def authorize_bot():
# 	client_id = os.environ.get('CLIENT_ID', config('CLIENT_ID'))
# 	url = f'https://api.imgur.com/oauth2/authorize?client_id={client_id}&response_type=token'
	# response = requests.request("GET", url)
	# print(response.text)
	# data = urlparse(response.url.fragment.split('&'))
	# print(data)
