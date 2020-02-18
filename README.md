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

### AWS Redshift cluster launching
The Redshift IAM role and cluster details can be launched programmatically or manually

### Python files to run ETL once the Redshift cluster has been deployed
- sql_queries.py
- create_tables.py
- etl.py

# License
Please feel free to base your work from this open repository, provide credit where appropriate.

### External links:
Redshift: COPY from JSON Format
https://docs.aws.amazon.com/redshift/latest/dg/copy-usage_notes-copy-from-json.html

Common pitfalls using RedShift (NOT NULL)
https://heap.io/blog/engineering/redshift-pitfalls-avoid

