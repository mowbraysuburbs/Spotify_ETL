import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import boto3  
from datetime import datetime
import json
import datetime

# s3 = boto3.client('s3')

bucket_name = "playlist-songs-spotify"

#Address for playlist
playlists_vault = {'rap_caviar': 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'}

#for naming csv file
playlist_name = list(playlists_vault.keys())[0]
datelabel = datetime.datetime.now().date().strftime("%Y%m%d")
filename = f"{datelabel}_Spotify_playlist_{playlist_name}.csv"

def lambda_handler(event, context):

  CLIENT_ID = "Your ID here"
  CLIENT_SECRET = "Your ID here"

  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=CLIENT_ID,
                                                  client_secret=CLIENT_SECRET))

  #stores in AWS lambda temp folder
  tmp_file = f"/tmp/{filename}"

  #gets info off all songs in playlist
  playlist = sp.playlist_items(playlist_id = playlists_vault['rap_caviar'])

  #objects wants from json spotify file
  columns = ['uri', 'date_added', 'main_artist', 'track_name', 'popularity']

  #write csv file 
  with open(tmp_file, 'w', newline = '') as file:
      writer = csv.DictWriter(file, fieldnames = columns)
      writer.writeheader()

      #req. for making csv file
      spotifyplaylist_json = {}

      for song in playlist['items']: 

          spotifyplaylist_json['uri'] = song['track']['uri']
          spotifyplaylist_json['date_added'] = song['added_at'].split("T")[0]
          spotifyplaylist_json['main_artist'] = song['track']['album']['artists'][0]['name']
          spotifyplaylist_json['track_name'] = song['track']['name']
          spotifyplaylist_json['popularity'] = song['track']['popularity']  

          writer.writerow(spotifyplaylist_json)

  aws_s3 = boto3.resource('s3')
  aws_s3.Object(bucket_name, filename).upload_file(tmp_file)


  print("Complete")

