#pyspark functions
from pyspark.sql.functions import *
from pyspark.sql import functions
from pyspark.sql.functions import round, col
import urllib

# Get AWS key from databricks storage
file_type = "csv"
first_row_is_header = "true"
delimiter = ","

# Read the CSV file to spark dataframe
aws_keys_df = spark.read.format(file_type)\
.option("header", first_row_is_header)\
.option("sep", delimiter)\
.load("/FileStore/tables/new_user_credentials.csv")

# Get the AWS access key and secret key from the spark dataframe
ACCESS_KEY = aws_keys_df.where(col('User name')=='nomar').select('Access key ID').collect()[0]['Access key ID']
SECRET_KEY = aws_keys_df.where(col('User name')=='nomar').select('Secret access key').collect()[0]['Secret access key']
# Encode the secret key
ENCODED_SECRET_KEY = urllib.parse.quote(string=SECRET_KEY, safe="")

# AWS S3 bucket name
AWS_S3_BUCKET = "audio-features-spotify"
# Mount name for the bucket
MOUNT_NAME = "/mnt/audio-features-spotify"
# Source url
SOURCE_URL = "s3n://{0}:{1}@{2}".format(ACCESS_KEY, ENCODED_SECRET_KEY, AWS_S3_BUCKET)
# Mount the drive
dbutils.fs.mount(SOURCE_URL, MOUNT_NAME)
# dbutils.fs.mount(SOURCE_URL)

# File locations and type
file_location = "/mnt/audio-features-spotify"
file_type = "csv"
# CSV options                                        
infer_schema = "true"
first_row_is_header = "true"
delimiter = ","

# The applied options are for CSV files. For other file types, these will be ignored.
df = spark.read.format(file_type) \
  .option("inferSchema", infer_schema) \
  .option("header", first_row_is_header) \
  .option("sep", delimiter) \
  .load(file_location)

# display(df)

#Spotify audio features
columns = ["danceability", 
           "energy", 
           "key", 
           "mode", 
           "speechiness", 
           "acousticness", 
           "instrumentalness", 
           "liveness", 
           "valence", 
           "tempo", 
           "duration_ms", 
           "time_signature", 
           "popularity"]

#Clear folder so new files can be inserted
dbutils.fs.rm(f"dbfs:/temp/", True)

for audio_feature in columns:
    single_audio_feature = df.select("date", audio_feature)
    
    #get stats    
    single_audio_feature_stats = single_audio_feature.groupBy('date').agg(
                              functions.min(audio_feature),
                              functions.max(audio_feature),
                              functions.stddev(audio_feature), 
                              functions.mean(audio_feature))
    
    #Format date
    single_audio_feature_stats = single_audio_feature_stats.withColumn(
        "date",date_format("date", "MM-dd-yyyy")) 
    
    #creating table for each audio feature
    for c in single_audio_feature_stats.columns[1:]:
        single_audio_feature_stats = single_audio_feature_stats.select("*", round(c,3))
        single_audio_feature_stats = single_audio_feature_stats.drop(c)
        single_audio_feature_stats = single_audio_feature_stats.withColumnRenamed(f"round({c}, 3)",c)
    
    #Group partitions into one file 
    single_audio_feature_stats = single_audio_feature_stats.coalesce(1)    
    
    #Save as csv
    filename = f"/temp/spotify-{audio_feature}-stats"                            
    df_to_csv = single_audio_feature_stats.write.format('csv') \
    .mode('overwrite').option("header", "true").save(filename)

#Finding and dislaying csv files for download and use   
for subfiles in dbutils.fs.ls("dbfs:/temp/"):
    prefix = "dbfs:/temp/"
    audio_feature_csv_file = dbutils.fs.ls(prefix + subfiles.name)
    
    #Ignores DBIO transactional commit, metadata files and selects csv file
    for csv in audio_feature_csv_file:
        if csv.name[-4:] == ".csv":
            print(csv.path)
            display_csv = spark.read.csv(csv.path, header = True)
            display(display_csv)