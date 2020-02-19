# AWS_Redshift_ETL

The purpose of this exercise is to demonstrate an ETL process using AWS Redshift.
Extract:
JSON files from S3 buckets
Transform:
Transforms data files into dimensional tables for analytics purposes using a star schema
Load:
Load into 5 dimensional tables

## Business context:
A music streaming startup, Sparkify, has grown their user base and song database and want to move their processes and data onto the cloud. Their data resides in S3, in a directory of JSON logs on user activity on the app, as well as a directory with JSON metadata on the songs in their app.

As their data engineer, you are tasked with building an ETL pipeline that extracts their data from S3, stages them in Redshift, and transforms data into a set of dimensional tables for their analytics team to continue finding insights in what songs their users are listening to.

### Python libraries imported:
import configparser
import psycopg2

### AWS credentials in dws.cfg variables
```
[CLUSTER]
HOST=
DB_NAME=
DB_USER= 
DB_PASSWORD=
DB_PORT= 

[IAM_ROLE]
ARN=

[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
```
### AWS Redshift cluster launching
The Redshift IAM role and cluster details can be launched programmatically or manually

### Python files to run ETL once the Redshift cluster has been deployed
- sql_queries.py
- create_tables.py
- etl.py
- ERD for Sparkify.pdf

### Database schema
The transformation of data into a star schema has the purpose to facilitate the analysis of the data in the JSON files.
Note in the sql_queries file how the staging tables don't require primary keys or specific constraints.
But the dimensional tables do need to respect the data types of the loaded information.
See attached star schema (ERD for Sparkify.pdf) for a graphical representation.

### Distribution strategy (DISTKEY and SORTKEY)
I have used a DISTKEY for song_id (as it seems that it will be a frequently joined field) in the tables songplays and songs
SORTKEY was used in all 5 tables for the fields: artist_id, user_id, start_time
Finally, I marked in the dimensional tables the PRIMARY KEYs for users to be able to use the dimensional tables once loaded.

### Explanation of the files in the repository
2 datasets are located in the S3 buckets
Where the files are in JSON format and contains metadata about a song and the artist of that song:
Song data: s3://udacity-dend/song_data
Log data: s3://udacity-dend/log_data

The Log dataset consists of log files in JSON format, this simulates app activity logs from the imaginary music streaming app Sparkify based on configuration settings. The log files in the dataset you'll be working with are partitioned by year and month:
Log data json path: s3://udacity-dend/log_json_path.json

# License
Please feel free to base your work from this open repository, provide credit where appropriate.

### External links:
Redshift: COPY from JSON Format
https://docs.aws.amazon.com/redshift/latest/dg/copy-usage_notes-copy-from-json.html

Common pitfalls using RedShift (NOT NULL)
https://heap.io/blog/engineering/redshift-pitfalls-avoid

