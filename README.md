
# Spotify's Rap Caviar playlist ETL pipeline using AWS (and Databricks)


**Using an ETL pipeline to investigate the change in hip-hop/rap genre over time**

---

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
This project seeks to investigate any change in the hip-hop/rap over time based on the playlist, 'Rap Caviar's overall audio features using an ETL process on Amazon Web Services (AWS) and Databricks.

### Background
Rap Caviar is one of the most popular playlists Spotify has on its platform. It consists of songs mainly from the hip-hop/rap genre. One could argue that this playlist is a good representation of the hip/hop rap genre. With any music genre, it changes and develops over time based on various factors such as culture, technology, influences of other genres, etc.

When you upload a song to Spotify, assigns various attributes or audio features to the song which is used for automated music recommendations. More information regarding Spotify audio features can be seen [here](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features)

Assuming that Rap Caviar is a good representation of the hip/hop rap genre,  The playlist's audio features is based on the average audio features (and other statistical values) from all the tracks in the playlists. This will be achieved by creating a ETL pipeline using AWS which scrapes and transforms this data i.e. audio features from Spotify's API every week. After significant amount of weeks have passed, one will be able to see any changes within the genre.

### Technologies
- AWS Lambda
- AWS S3
- AWS Identity and Access Management (IAM)
- AWS Cloudwatch
- Databricks
- Python

### ETL Pipeline

![[Pasted image 20220826213255.png]]

### Data Model
![[Pasted image 20220826213500.png]]

## Installation 
### Spotify API
First need to create an account with Spotify for Developers [here](https://developer.spotify.com/dashboard/). Thereafter, create an app to get your account's Client ID and Client Secret ID.

### Identity and Access Management (IAM)
AWS Access Key and Secret Key is required for Databricks to read files within the S3 bucket in your AWS account. This can be done by creating a user under the 'Access management-Users' tab. 

Configurations to be used when making user:
- AWS type: Programmatic access 
- Permissions: 'AmazonS3FullAccess'

Once the user has been created, download credential information of your account (in a .csv format). This contains your information such as your access key ID and Secret access key. This file will be used in the Databricks cluster.

### Lambda Functions 
Both lambda functions extract data from the Spotify API. Details regarding each function are as follows:

Lambda function 1
- Name: Spotify_playlist_items_function
- Function: Extracts song information from the 'Rap Caviar' playlist (refer to data model)
- Trigger: CloudWatch
- Runtime: Python 3.9
- Architecture: x86_64
- Timeout time: 1min (Previously 3s)

Lambda function 2
- Name: Spotify_audio_features_function
- Function: Extracts song information from the 'Rap Caviar' playlist (refer to data model)
- Trigger: S3 Bucket (Event Type: PUT)
- Runtime: Python 3.9
- Architecture: x86_64
- Timeout time: 1min (Previously 3s)

![[Pasted image 20220826000052.png]]


AWS Lambda did not have all the all the Python packages to run the code. Therefore required packages were require to be placed in the environment as well in a layer. The following Python packages were required:

- redis
- spotipy
- requests

Two layers are required to placed on both Lambda functions: A layer consisting of the relevant Python packages and the AWS layer, 'ÁWSDataWrangler-Python39' which is already created. When creating the Python package layer, use the 'python packages.zip' zip file in the repo. 

### Triggers

#### Cloudwatch (EventBridge)
A rule is required to trigger the the first lambda function i.e. "Spotify_playlist_items_function" activates it every week (7 days). Subsequently, the lambda function extracts all the songs in the playlist for that week. Refer below for rule configuration.  

![[Pasted image 20220824181152.png]]

#### S3 Bucket 
As previously mentioned, the second lambda function, 'Spotify_audio_features_function' takes some the output from the first lambda function, 'Spotify_playlist_items_function' and uses it to retrieve the audio feature characteristics of all the songs from the playlist. Subsequently, the second lambda function can only begin once the first function lambda function is completed. The first lambda function is completed once is has stored a .csv file in the S3 bucket. Thus we can use this S3 bucket to trigger the second lambda function. See below regarding the s3 trigger details. Note that it is an PUT event type. 

![[Pasted image 20220823224218.png]]


### Databricks
Databricks is an cloud-based tool used to process and transform large quantities of data. It has similar properties and functions as the AWS Glue package.  

Databricks community edition, the free version provided by Databricks, was used for this project. As it is a free version, it provides limited access to all the features of Databricks. These limitations will be mentioned in the following.  

As mentioned previously, the AWS account's credential information file (containing access and secret key) was retrieved from AWS IAM and will be used to mount the S3 bucket to Databricks cluster to read files. 

Before we can begin to code in Databricks, a cluster needs to be created. In Databricks UI, click the Compute icon to create new cluster. Please below regarding cluster configuration information. 

![[Pasted image 20220824215851.png]]

Once the cluster has been created, your AWS credential information file can be uploaded to Databricks. Click the Data icon and then click the Create Table button. Drag or upload your credential information file onto Databricks. See below for storage information. Note the DBFS Target Directory. This will be the location of the credential information file .

![[Pasted image 20220824215205.png]]

The code was written using Pyspark. Create a notebook to begin your code. The ETL process of Databricks is not automated due to the free subscription limitations. It is recommended that you use AWS Glue to automate the process however, it will incur costs. Copy the code from file ''Databricks_ETL_Pyspark.py" into the notebook and run to get the statistical result data.Transformed data will be in csv format for each audio feature and can be retrieved by clicking the download button.

![[Pasted image 20220825234406.png]]


![[Pasted image 20220825234844.png]]

## References

### AWS Glue Tutorial
https://www.youtube.com/watch?v=taR2hRZ2AwI&list=LL&index=5

### # AWS Glue Tutorial for Beginners
https://www.youtube.com/watch?v=dQnRP6X8QAU&list=LL&index=25

### Add triggers to AWS Glue from S3
https://stackoverflow.com/questions/48828194/event-based-trigger-of-aws-glue-crawler-after-a-file-is-uploaded-into-a-s3-bucke

### Create single file in AWS Glue (pySpark) and store as custom file name S3
https://learnsqlteam.com/2021/07/18/create-single-file-in-aws-glue-pyspark-and-store-as-custom-file-name-s3/

### write csv file into one file by pyspark
https://stackoverflow.com/questions/36574617/how-to-write-csv-file-into-one-file-by-pyspark

### Rename a PySpark dataframe column by index
https://www.geeksforgeeks.org/how-to-rename-a-pyspark-dataframe-column-by-index/

### Musicstax 
https://musicstax.com/

### Spotify Popularity — A unique insight into the Spotify algorithm and how to influence it
https://lab.songstats.com/spotify-popularity-a-unique-insight-into-the-spotify-algorithm-and-how-to-influence-it-93bb63863ff0

### AWS get files without getting folders
https://stackoverflow.com/questions/42673764/boto3-s3-get-files-without-getting-folders

### Mount S3 to Databricks
https://www.youtube.com/watch?v=jKUBwgIcK7g

### PySpark For AWS Glue Tutorial
https://www.youtube.com/watch?v=DICsZiwuHJo

### PySpark groupby mean function
https://spark.apache.org/docs/latest/api/python/reference/pyspark.pandas/api/pyspark.pandas.groupby.GroupBy.mean.html

### Pyspark round function
https://www.educba.com/pyspark-round/

### Download Data From Databricks (DBFS) to Local System
https://www.youtube.com/watch?v=PdLpXhK4u8w

### 
https://sparkbyexamples.com/pyspark/pyspark-read-csv-file-into-dataframe/
https://medium.com/grabngoinfo/databricks-mount-to-aws-s3-and-import-data-4100621a63fd

### Databricks Mount To AWS S3 And Import Data
https://www.youtube.com/watch?v=jKUBwgIcK7g&list=LL&index=19

### PySpark single .csv file
https://stackoverflow.com/questions/65954797/how-to-save-pyspark-data-frame-in-a-single-csv-file

### _STARTED_, _COMMITTED_ , and _SUCCESS_ files in a Spark
https://stackoverflow.com/questions/68196969/what-are-the-started-committed-and-success-files-in-a-spark-parquet-tab

### Multiple criteria for aggregation on PySpark Dataframe
https://www.geeksforgeeks.org/multiple-criteria-for-aggregation-on-pyspark-dataframe/

### Read CSV files - Pyspark 
https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql/api/pyspark.sql.DataFrameReader.csv.html#pyspark.sql.DataFrameReader.csv

### Pyspark change date format
https://stackoverflow.com/questions/70856553/changing-date-format-in-pyspark
<!-- 
### Dataframe to .csv
https://www.golinuxcloud.com/convert-pandas-dataframe-to-csv/ -->

### AWS Lambda "errorMessage": Task timed out after 3.00 seconds
https://stackoverflow.com/questions/62948910/aws-lambda-errormessage-task-timed-out-after-3-00-seconds

### Github - Data Lake on AWS ingested by Spotify APIs
https://github.com/abhinavjainn/spotify-aws-data-lake

### Create a CSV in Lambda using Python?
https://newbedev.com/how-do-i-create-a-csv-in-lambda-using-python

### Writing CSV Files with csv.writer and DictWriter
https://www.youtube.com/watch?v=jnkPnNaLY3g

### Upload to S3 From Lambda
https://www.youtube.com/watch?v=vXiZO1c5Sk0

---
