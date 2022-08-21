# Spotify_ETL

## Summary
Rap Caviar is one of the most popular playlists Spotify has on its platform. It consists of songs mainly from the hip-hop/rap genre. One could argue that this playlist is a good representation of the hip/hop rap genre. The hip/hop rap genre changes and develops over time based on various factors such as culture, technology, influences of other genres, etc. 

When you upload a song to Spotify, assigns various attributes or audio features to the song which is used for automated music recommendations. More information regarding Spotify audio features can be seen here: (https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

Assuming that Rap Caviar is a good representation of the hip/hop rap genre, this project seeks to investigate any change in the genre over time based on the playlist's audio features.  The playlist's audio features is based on the average audio features (and other statistical values) from all the tracks in the playlists. This will be achieved by creating a ETL pipeline using AWS which scrapes and transforms this data i.e. audio features from Spotify's API every week. After significant amount of weeks have passed, one will be able to see any changes within the genre.


## TODO 

Note:
I do not know whether this is the best way or the correct method of doing things. List will be amended as I progress thru the project. 

- Extract playlist from Spotify API on a weekly base using AWS (using AWS Lambda (I think) for the extraction and the automate this weekly using Amazon CloudWatch Events (I think) )
- Send raw data from Spotify API into AWS S3 - This will be the data lake
- Convert the songs in the playlists to find the common statistical values (mean, medium, std dev, etc) based on the Spotify songs attributes using AWS Glue and Apache Spark
- Place transformed data into another S3 (this is will the data warehouse)
- Use transformed data for dashboard in Tableau

## ETL Diagram

![image](https://user-images.githubusercontent.com/60255967/185808716-15d44fd6-0143-4339-9038-da88b3ac193d.png)


## Data Model

![image](https://user-images.githubusercontent.com/60255967/185810837-a497a8ac-ba25-4ed6-af81-912e5fd4fd51.png)

