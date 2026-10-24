import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine



def load_articles(articles_df):

    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_NAME = os.getenv('DB_NAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')


    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    articles_df.to_sql('articles_main', con = engine, if_exists='replace', index=False)
