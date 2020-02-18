# This etl.py file contains the libraries, functions and main function to kick start the ETL process in Redshift
# Here I load the 2 libraries and the the sql_queries file
import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

# Here I load the 2 staging tables using the script for copy_table_queries from the sql_queries file
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

# Here I insert data into the 5 tables using the script for insert_table_queries from the sql_queries file
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

# This main function connects to the Redshift cluster using my credentials from the dwh.cfg file
# Note my credentials are not included in the file
# Then it sets the 2 functions to run loading staging tables and inserting data into the 5 tables
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()