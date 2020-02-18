# The ConfigParser class implements a basic configuration file parser language for ease of use for the creation of SQL queries
import configparser


# We use the config class to read the dwh.cfg file where AWS credentials are located
config = configparser.ConfigParser()
config.read('dwh.cfg')

# S3 location of the json files for logs, log data json path, songs, and IAM role
LOG_DATA        = config.get('S3', 'LOG_DATA')
LOG_JSONPATH    = config.get('S3', 'LOG_JSONPATH')
SONG_DATA       = config.get('S3', 'SONG_DATA')
ARN             = config.get('IAM_ROLE', 'ARN')

# To ensure a clean deployment each time I launch the cluster here I'm dropping the tables

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# Here I create the 2 staging tables for the events and songs
# Redshift doesn't require primary keys, the below doesn't include a distribution strategy
# Notice how for the staging tables is not necessary to add specific constraints such as NOT NULL
staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
artist VARCHAR,
auth VARCHAR,
firstName VARCHAR,
gender VARCHAR,
iteminSession VARCHAR,
lastName VARCHAR,
length VARCHAR,
level VARCHAR,
location VARCHAR,
method VARCHAR,
page VARCHAR,
registration VARCHAR,
sessionId INT,
song VARCHAR,
status INT,
ts BIGINT,
userAgent VARCHAR,
userId INT
);
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs (
num_songs INT,
artist_id VARCHAR,
artist_latitude NUMERIC,
artist_longitude NUMERIC,
artist_location VARCHAR,
artist_name VARCHAR,
song_id VARCHAR,
title VARCHAR,
duration NUMERIC,
year INT
);
""")

# Here I create the 5 tables: songplays, users, songs, artists and time

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS songplays(
songplay_id INT,
start_time TIMESTAMP NOT NULL,
user_id INT NOT NULL,
level VARCHAR NOT NULL,
song_id VARCHAR NOT NULL,
artist_id VARCHAR NOT NULL,
session_id INT NOT NULL,
location VARCHAR NOT NULL,
user_agent VARCHAR NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS users (
user_id INT NOT NULL,
first_name VARCHAR NOT NULL,
last_name VARCHAR NOT NULL,
gender CHAR NOT NULL,
level VARCHAR NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS songs (
song_id VARCHAR NOT NULL,
title VARCHAR NOT NULL,
artist_id VARCHAR NOT NULL,
year INT NOT NULL,
duration FLOAT NOT NULL
);
""")

# Notice that location, latitude and longitude can be null values
artist_table_create = ("""
CREATE TABLE IF NOT EXISTS artists (
artist_id VARCHAR NOT NULL,
name VARCHAR NOT NULL,
location VARCHAR,
latitude NUMERIC,
longitude NUMERIC
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS time (
start_time TIMESTAMP NOT NULL,
hour INT NOT NULL,
day INT NOT NULL,
week INT NOT NULL,
month INT NOT NULL,
year INT NOT NULL,
weekday INT NOT NULL
);
""")

# Here I load the data into the staging tables using my credentials from the dwh.cfg file

staging_events_copy = ("""
COPY staging_events FROM {}
CREDENTIALS 'aws_iam_role={}'
FORMAT AS json {}
region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
COPY staging_songs FROM {}
CREDENTIALS 'aws_iam_role={}'
FORMAT AS json 'auto'
region 'us-west-2';
""").format(SONG_DATA, ARN)

# Here I'm loading the data from the stating tables to the 5 different tables

songplay_table_insert = ("""
INSERT INTO songplays (
start_time,
user_id,
level,
song_id,
artist_id,
session_id,
location,
user_agent)
SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
se.userId AS user_id,
se.level,
ss.song_id ,
ss.artist_id,
se.sessionId AS session_id,
se.location,
se.userAgent AS user_agent
FROM staging_events se
JOIN staging_songs ss
ON se.song = ss.title AND se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (
user_id,
first_name,
last_name,
gender,
level
)
SELECT DISTINCT 
se.userId AS user_id,
se.firstName AS first_name,
se.lastName AS last_name,
se.gender AS gender,
se.level AS level
FROM staging_events se
WHERE se.page ='NextSong';
""")

song_table_insert = ("""
INSERT INTO songs (
song_id,
title,
artist_id,
year,
duration
)
SELECT DISTINCT
ss.song_id,
ss.title,
ss.artist_id,
ss.year,
ss.duration
FROM staging_songs ss;
""")

artist_table_insert = ("""
INSERT INTO artists (
artist_id,
name,
location,
latitude,
longitude)
SELECT DISTINCT
ss.artist_id AS artist_id,
ss.artist_name AS name,
ss.artist_location AS location,
ss.artist_latitude AS latitude,
ss.artist_longitude AS longitude
FROM staging_songs ss;
""")

time_table_insert = ("""
INSERT INTO time (
start_time,
hour,
day,
week,
month,
year,
weekday)
SELECT DISTINCT TIMESTAMP 'epoch' + se.ts/1000 * INTERVAL '1 second' AS start_time,
EXTRACT(hour FROM start_time) AS hour,
EXTRACT(day FROM start_time) AS day,
EXTRACT(week FROM start_time) AS week,
EXTRACT(month FROM start_time) AS month,
EXTRACT(year FROM start_time) AS year,
EXTRACT(week FROM start_time) AS weekday
FROM staging_events se
WHERE se.page = 'NextSong';
""")

# These are the list of queries to be used in the create_tables.py and etl.py files

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
