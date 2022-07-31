import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import boto3  
from datetime import datetime
import json
import datetime
import requests

s3 = boto3.client('s3')
bucket_name = "spotifydatalake"


playlists_vault = {'rap_caviar': 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'}

#for naming csv file
playlist_name = list(playlists_vault.keys())[0]
datelabel = datetime.datetime.now().date().strftime("%Y%m%d")
filename = f"{datelabel}_Spotify_audiofeatures_{playlist_name}.csv"

def lambda_handler(event, context):

  #stores in lambda temp folder
  tmp_file = f"/tmp/{filename}"

  sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="c24b9f9df8a04725bcf2e0e8538be3a6",
                                                        client_secret="8c5cb06ac1ac46e19f37bc9d6b323695"))
                                                        
  #gets info off all songs in playlist
  playlist = sp.playlist_items(playlist_id = playlists_vault['rap_caviar'])

  playlist_uri = []

  for info in playlist['items']:
      uri = info['track']['uri']
      playlist_uri.append(uri)

  #Gets audios features from playlist
  playlist_features = sp.audio_features(tracks=playlist_uri)

  #spotify audio features
  columns = ['uri','date', 'danceability', 'energy', 
          'key', 'mode', 'speechiness', 
          'acousticness', 'instrumentalness', 'liveness', 
          'valence', 'tempo', 'duration_ms', 'time_signature']

  with open('test.csv', 'w', newline = '') as file:
      writer = csv.DictWriter(file, fieldnames = columns)
      writer.writeheader()

      spotify_json = {}
      for i in range(0,len(playlist_features)): 

          spotify_json['uri'] = playlist_features[i]['uri']  
          spotify_json['date'] = current_date = datetime.datetime.today().date()
          spotify_json['danceability'] = playlist_features[i]['danceability']
          spotify_json['energy'] = playlist_features[i]['energy'] 
          spotify_json['key'] = playlist_features[i]['key']  
          spotify_json['mode'] = playlist_features[i]['mode']
          spotify_json['speechiness'] = playlist_features[i]['speechiness'] 
          spotify_json['acousticness'] = playlist_features[i]['acousticness']  
          spotify_json['instrumentalness'] = playlist_features[i]['instrumentalness'] 
          spotify_json['liveness'] = playlist_features[i]['liveness'] 
          spotify_json['valence'] = playlist_features[i]['valence']  
          spotify_json['tempo'] = playlist_features[i]['tempo'] 
          spotify_json['duration_ms'] = playlist_features[i]['duration_ms'] 
          spotify_json['time_signature'] = playlist_features[i]['time_signature']
      
          writer.writerow(spotify_json)

  s3.put_object(Bucket = bucket_name, Key = filename, Body = file)

  print("Complete")

