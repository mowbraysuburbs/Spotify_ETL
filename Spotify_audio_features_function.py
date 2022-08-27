import spotipy
import csv
from spotipy.oauth2 import SpotifyClientCredentials
import boto3  
from datetime import datetime
import json
import datetime
import requests 

s3_client = boto3.client("s3")

def lambda_handler(event, context):
    
    #getting uri and popularity rating from csv file that entered s3 bucket
    bucket_name = event["Records"][0]["s3"]["bucket"]["name"]
    s3_file_name = event["Records"][0]["s3"]["object"]["key"] 

    resp = s3_client.get_object(Bucket=bucket_name, Key=s3_file_name)
    
    data = resp["Body"].read().decode("utf-8")
    
    uri = [] #uri codes
    pop = [] #popularity ratings
    songs = data.split("\n")
    
    for song in songs:
    
        song_data = song.split(",",2)
        
        uri_items = song_data[0]
        pop_items = song_data[-1].split(",")[-1]
        
        uri.append(uri_items)
        pop.append(pop_items)
    
    
    bucket_name = "audio-features-spotify"

    CLIENT_ID= "c24b9f9df8a04725bcf2e0e8538be3a6"
    CLIENT_SECRET = "8c5cb06ac1ac46e19f37bc9d6b323695"
    
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
                        client_id=CLIENT_ID, 
                        client_secret= CLIENT_SECRET)
                        )

    playlists_vault = {'rap_caviar': 'spotify:playlist:37i9dQZF1DX0XUsuxWHRQd'}

    #for naming csv file
    playlist_name = list(playlists_vault.keys())[0]
    datelabel = datetime.datetime.now().date().strftime("%Y%m%d")
    filename = f"{datelabel}_Spotify_audiofeatures_{playlist_name}.csv"

#   #stores in lambda temp folder
    tmp_file = f"/tmp/{filename}"

#   #Gets audios features from playlist
    playlist_features = sp.audio_features(tracks=uri[1:len(uri)])
     
    for i in playlist_features:
        print(i)
    
#   #spotify audio features
    columns = ['uri','date', 'danceability', 'energy', 
            'key', 'mode', 'speechiness', 'acousticness', 
            'instrumentalness', 'liveness', 'valence', 'tempo', 
            'duration_ms', 'time_signature', "popularity"]

    with open(tmp_file, 'w', newline = '') as file:
        writer = csv.DictWriter(file, fieldnames = columns)
        writer.writeheader()
    
        spotify_json = {}
        pop = pop[1:len(pop)]
        
        for i in range(0,len(playlist_features)): 
    
            spotify_json['uri'] = playlist_features[i]['uri']  
            spotify_json['date'] = current_date = datetime.datetime.today().date()
            spotify_json['danceability'] = float(playlist_features[i]['danceability'])
            spotify_json['energy'] = float(playlist_features[i]['energy'])
            spotify_json['key'] = int(playlist_features[i]['key'])  
            spotify_json['mode'] = int(playlist_features[i]['mode'])
            spotify_json['speechiness'] = float(playlist_features[i]['speechiness'])
            spotify_json['acousticness'] = float(playlist_features[i]['acousticness'])
            spotify_json['instrumentalness'] = float(playlist_features[i]['instrumentalness'])
            spotify_json['liveness'] = float(playlist_features[i]['liveness'])
            spotify_json['valence'] = float(playlist_features[i]['valence']) 
            spotify_json['tempo'] = float(playlist_features[i]['tempo'])
            spotify_json['duration_seconds'] = float(playlist_features[i]['duration_ms']/1000)
            spotify_json['time_signature'] = int(playlist_features[i]['time_signature'])
            spotify_json['popularity'] = float(int(pop[i]))  

            writer.writerow(spotify_json)

    aws_s3 = boto3.resource('s3')
    aws_s3.Object(bucket_name, filename).upload_file(tmp_file)
    

    print("Complete")

