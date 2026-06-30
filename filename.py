import os
from pyyoutube import Client
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

client = Client(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

url, state = client.get_authorize_url()
print('Authorize: ', url)

redirect_url = input('Redirect: ')
access_token = client.generate_access_token(authorization_response=redirect_url)

video_id = input('Enter Video ID: ')
response = client.videos.rate(video_id, rating="like")
print(response)

rating = client.videos.get_rating(video_id=video_id)
print(rating)