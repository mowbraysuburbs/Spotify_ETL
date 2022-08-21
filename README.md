# Spotify_ETL

## Summary
Rap Caviar is one of the most popular playlists Spotify has on its platform. It consists of songs mainly from the hip-hop/rap genre. One could argue that this playlist is a good representation of the hip/hop rap genre. The hip/hop rap genre changes and develops over time based on various factors such as culture, technology, influences of other genres, etc. 

When you upload a song to Spotify, assigns various attributes or audio features to the song which is used for automated music recommendations. More information regarding Spotify audio features can be seen here: (https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

Assuming that Rap Caviar is a good representation of the hip/hop rap genre, this project seeks to investigate any change in the genre over time based on the playlist's audio features.  The playlist's audio features is based on the average audio features (and other statistical values) from all the tracks in the playlists. This will be achieved by creating a ETL pipeline using AWS which scrapes and transforms this data i.e. audio features from Spotify's API every week. After significant amount of weeks have passed, one will be able to see any changes within the genre.



## ETL Diagram

![image](https://user-images.githubusercontent.com/60255967/185808716-15d44fd6-0143-4339-9038-da88b3ac193d.png)


## Data Model

![image](https://user-images.githubusercontent.com/60255967/185810893-9a061205-4751-4fc7-bd45-5e06c86c49c4.png)

