import pandas as pd

def transform_articles(articles):
    articles_df = pd.DataFrame(articles)
    articles_df.head()
    articles_df = articles_df.drop(columns={'source','urlToImage'})

    return articles_df