# Spotify's Rap Caviar playlist ETL pipeline using AWS (...& Databricks)

<p align="center">
  <img src="https://www.pc.co.il/wp-content/uploads/2016/06/AWS600.jpg" />
</p>

<p align="center">
Using an ETL pipeline to investigate the change in hip-hop/rap genre over time (Remind me to check on this repo in a year so I can provide a fancy graph).
</p>

## Table of Contents
- [Introduction](#introduction)
	- [Purpose](#purpose)
	- [Background](#background)
	- [Technologies](#technologies)
	- [ETL Pipeline](#etl-pipeline)
	- [Data Model](#data-model)
- [Installation](#installation)
	- [Spotify API](#spotify-api)
	- [Identity and Access Management (IAM)](#identity-and-access-management-iam)
	- [Lambda Functions](#lambda-functions)
	- [Triggers](#triggers)
- [References](#references)

## Introduction
### Purpose
This project investigate any change in hip-hop/rap over time based on Spotify's playlist, '[Rap Caviar](https://open.spotify.com/playlist/37i9dQZF1DX0XUsuxWHRQd)'s overall audio features statistical values (i.e. mean, std, max & min) using an ETL process on Amazon Web Services (AWS) and Databricks.

### Background
Rap Caviar is one of the most popular playlists on Spotify. It consists of songs mainly from the hip-hop/rap genre. You could argue that this playlist is a good representation of the hip-hop/rap genre. As with any music genre, it changes and develops over time based on various factors such as culture, technology, influences of other genres, etc.

When you upload a song to Spotify, assigns various [audio features](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features) to the song which is used for automated song recommendations. Assuming that Rap Caviar is a good representation of the hip/hop rap genre, The playlist's audio features are based on the average audio features (and other statistical values) from all the tracks in the playlists. This will be achieved by creating an ETL pipeline using AWS, which scrapes and transforms this data i.e. audio features from Spotify's API every week. After a significant amount of weeks have passed, one will be able to see any changes within the genre.

### Technologies
- AWS Lambda
- AWS S3
- AWS Identity and Access Management (IAM)
- AWS Cloudwatch
- Databricks
- Python
- PySpark

### ETL Pipeline
![image](https://user-images.githubusercontent.com/60255967/187020773-7afaeae8-6117-4694-8b77-5a560f1470c3.png)

### Data Model
![image](https://user-images.githubusercontent.com/60255967/187020801-e22fdbed-c1ff-4a1c-b11e-e960b7101f3d.png)

*(Return to [Table of Contents](#table-of-contents))*

## Installation 
### Spotify API
First, need to create an account with [Spotify for Developers](https://developer.spotify.com/dashboard/). Thereafter, create an app to get your account's Client ID and Client Secret ID.

### Identity and Access Management (IAM)
AWS Access Key and Secret Key are required for Databricks to read files within the S3 bucket in your AWS account. Create a user under the 'Access management-Users' tab. Once the user has been created, download the credential information of your account (in a .csv format). 

Configurations to be used when making user:
- AWS type: Programmatic access 
- Permissions: 'AmazonS3FullAccess'

### Lambda Functions 
Both lambda functions extract data from the Spotify API.  Both lambda function scripts can be found in the repo. Upload to respective lambda function environment in the ZIP format provided. ZIP files contain the code as well as the required Python packages. The image below displays the outcome of the upload and details regarding each function are as follows:

<p align="center">
  <img src="https://user-images.githubusercontent.com/60255967/187020994-aa12e1c2-b78f-4204-bfcc-ea4d35a2c89f.png" />
</p>

**Lambda function 1**
- Name: Spotify_playlist_items_function
- Function: Extracts song information from the 'Rap Caviar' playlist (refer to data model)
- Trigger: CloudWatch
- Runtime: Python 3.9
- Architecture: x86_64
- Timeout time: 1min (Previously 3s)

**Lambda function 2**
- Name: Spotify_audio_features_function
- Function: Extracts audio features from a song list. In this case from the 'Rap Caviar' playlist (refer to data model)
- Trigger: S3 Bucket (Event Type: PUT)
- Runtime: Python 3.9
- Architecture: x86_64
- Timeout time: 1min (Previously 3s)

The main notion of both Lambda functions is it extracts data from Spotify API, stores that info in a CSV file, and uploads to or reads from an S3 bucket. The spotipy package is used to gain access to Spotify API. Place your Client ID and Client Secret ID in the provided fields.

```python 
from spotipy.oauth2 import SpotifyClientCredentials

  
CLIENT_ID= "your ID here"
CLIENT_SECRET = "your ID here"

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
					client_id=CLIENT_ID, 
					client_secret= CLIENT_SECRET)
					)
```
 
AWS Lambda did not have all the Python packages to run the code. Therefore required packages were required to be placed in the environment as well in a layer. The following Python packages were required:
- redis
- spotipy
- requests

Two layers are required to be placed on both Lambda functions: A layer consisting of the relevant Python packages and the AWS layer, 'ÁWSDataWrangler-Python39' which is already created. When creating the Python package layer, use the 'python packages.zip' zip file in the repo. 

*(Return to [Table of Contents](#table-of-contents))*

### Triggers

#### Cloudwatch (EventBridge)
A rule is required to trigger the first lambda function i.e. "Spotify_playlist_items_function" activates it every week (7 days). Refer below for the rule configuration.  

![image](https://user-images.githubusercontent.com/60255967/187021174-ae9b24c2-595b-42c6-852a-37977d2b3e9e.png)

#### S3 Bucket 
As shown in the ETL pipeline, the second lambda function, 'Spotify_audio_features_function' takes some of the output i.e. CSV file from the first lambda function, 'Spotify_playlist_items_function' and uses it to retrieve the audio feature characteristics of all the songs from the playlist. Thus we can use this S3 bucket to trigger the second lambda function. See below regarding the s3 trigger details. Note that it is a PUT event type. 

<p align="center">
  <img src="https://user-images.githubusercontent.com/60255967/187021216-ace4ad6b-7f3b-4b02-a827-688b4279650b.png" />
</p>

*(Return to [Table of Contents](#table-of-contents))*

### Databricks
Databricks community edition, a free version provided by Databricks, was used for this project. As mentioned previously, the AWS account's credential information file (containing access and secret key) was retrieved from AWS IAM and will be used to mount the S3 bucket to the Databricks cluster to read files. Create your cluster, thereafter, your AWS credential information file can be uploaded to Databricks. Click the Data icon and then click the Create Table button. Drag or upload your credential information file onto Databricks. See below for storage information. Note the DBFS Target Directory. This will be the location of the credential information file.

<p align="center">
  <img src="https://user-images.githubusercontent.com/60255967/187021435-1cde537f-233c-4363-8311-6464f329d5ca.png" />
</p>

The code was written using Pyspark. Create a notebook and copy code from 'Databricks_ETL_Pyspark.py" in the repo. For Databricks to gain access to the data, the S3 bucket will have to be mounted on the cluster. This will only need to be done once per cluster.

```python
dbutils.fs.mount(SOURCE_URL, MOUNT_NAME)
```
The main idea of this code is to mount/extract the S3 bucket onto the Databricks cluster, transform the data by conducting basic statistical aggregate functions on each audio feature and load each as a CSV file. The ETL process of Databricks is not automated possibly due to the free subscription limitations. CSV files for each audio feature will have to be downloaded. Refer to the image for details. 

![image](https://user-images.githubusercontent.com/60255967/187021487-ab873f7a-1c35-42f9-b63b-d41e8bb0161c.png)

*(Return to [Table of Contents](#table-of-contents))*

## References

**write csv file into one file by pyspark**   
https://stackoverflow.com/questions/36574617/how-to-write-csv-file-into-one-file-by-pyspark

**Rename a PySpark dataframe column by index**   
https://www.geeksforgeeks.org/how-to-rename-a-pyspark-dataframe-column-by-index/

**Musicstax**    
https://musicstax.com/

**Spotify Popularity — A unique insight into the Spotify algorithm and how to influence it**  
https://lab.songstats.com/spotify-popularity-a-unique-insight-into-the-spotify-algorithm-and-how-to-influence-it-93bb63863ff0

**AWS get files without getting folders**  
https://stackoverflow.com/questions/42673764/boto3-s3-get-files-without-getting-folders

**Mount S3 to Databricks**  
https://www.youtube.com/watch?v=jKUBwgIcK7g

**PySpark groupby mean function**  
https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/api/pyspark.pandas.groupby.GroupBy.mean.html

**Pyspark round function**  
https://www.educba.com/pyspark-round/

**Download Data From Databricks (DBFS) to Local System**  
https://www.youtube.com/watch?v=PdLpXhK4u8w

**Databricks Mount To AWS S3 And Import Data**  
https://www.youtube.com/watch?v=jKUBwgIcK7g&list=LL&index=19

**PySpark single .csv file**  
https://stackoverflow.com/questions/65954797/how-to-save-pyspark-data-frame-in-a-single-csv-file

**_STARTED_, _COMMITTED_ , and _SUCCESS_ files in a Spark**  
https://stackoverflow.com/questions/68196969/what-are-the-started-committed-and-success-files-in-a-spark-parquet-tab

**Multiple criteria for aggregation on PySpark Dataframe**  
https://www.geeksforgeeks.org/multiple-criteria-for-aggregation-on-pyspark-dataframe/

**Read CSV files - Pyspark**   
https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.csv.html#pyspark.sql.DataFrameReader.csv

**Pyspark change date format**  
https://stackoverflow.com/questions/70856553/changing-date-format-in-pyspark

**Dataframe to .csv**  
https://www.golinuxcloud.com/convert-pandas-dataframe-to-csv/

**AWS Lambda "errorMessage": Task timed out after 3.00 seconds**  
https://stackoverflow.com/questions/62948910/aws-lambda-errormessage-task-timed-out-after-3-00-seconds

**Github - Data Lake on AWS ingested by Spotify APIs**  
https://github.com/abhinavjainn/spotify-aws-data-lake

**Create a CSV in Lambda using Python?**  
https://newbedev.com/how-do-i-create-a-csv-in-lambda-using-python

**Writing CSV Files with csv.writer and DictWriter**
https://www.youtube.com/watch?v=jnkPnNaLY3g

**Upload to S3 From Lambda**  
https://www.youtube.com/watch?v=vXiZO1c5Sk0

**Create CSV in AWS Lambda**   
https://stackoverflow.com/questions/57429183/how-do-i-create-a-csv-in-lambda-using-python

*(Return to [Table of Contents](#table-of-contents))*
