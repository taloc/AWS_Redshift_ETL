# This create_tables.py file contains the libraries, functions and main function to create the tables
# Here I load the 2 libraries and the the sql_queries file
import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries

# Note that for the sake of this exercise I will drop all the tables to get a fresh start
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

# Here I create the staging tables and 5 tables by using the script associated to create_table_queries from the sql_queries file
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

# This main function connects to the Redshift cluster using my credentials from the dwh.cfg file
# Note my credentials are not included in the file
# Then it sets the 2 functions to drop any pre-existing tables with the same names I'll use in this exercise;
# it then runs the script to create the 2 staging tables and 5 tables
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()