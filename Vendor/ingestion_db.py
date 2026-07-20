import pandas as pd
import logging
from sqlalchemy import create_engine
import os
import time

logging.basicConfig(
    filename= "Vendor/logs/ingestion_db.log",
    level = logging.DEBUG,
    format= "%(asctime)s - %(levelname)s - %(message)s",
    filemode= "a"
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    '''This function will ingest the DataFrame into Database table'''
    df.to_sql(table_name, con = engine, if_exists='replace', index=False)

def load_raw_data():
    '''This function will load CSVs as DataFrame and ingest into DB'''
    start = time.time()
    for file in os.listdir('Vendor/data'):
        if '.csv' in file:
            df = pd.read_csv("Vendor/data/"+file)
            logging.info(f"Ingesting {file} into db")
            ingest_db(df, file[:-4], engine)
    
    end = time.time()
    total_time = (end - start) / 60
    logging.info("Ingestion complete")
    logging.info(f"\nTime taken: {total_time} minutes")

if __name__ == '__main__':
    load_raw_data()