import requests
import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine

load_dotenv()

def extract_articles():
    url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2026-05-11&'
       'sortBy=popularity&'
       'apiKey=' + os.getenv('NEWS_API_KEY'))

    response = requests.get(url)
    data = response.json()
    articles = data['articles']
    return articles