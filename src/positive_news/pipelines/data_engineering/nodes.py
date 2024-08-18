"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.7
"""
# =================
# ==== IMPORTS ====
# =================

import hopsworks
import pandas as pd
from newsdataapi import NewsDataApiClient

# ===================
# ==== FUNCTIONS ====
# ===================

def request_news(api_key: str, max_result: int=2) -> pd.DataFrame:
    """Request news in english language

    Args:
        api_key (str): API key used to request the news from NewsDataAPI
        max_result (int): Maximum number of results to request
    Returns:
        df_news (pd.DataFrame): Articles saved in a dataframe
    """
    #TODO update credentials load for Kedro
    # Create a NewsData API client
    client = NewsDataApiClient(apikey=api_key)

    # Collect articles from many countries in a list
    all_articles = []
    country_codes = ['us', 'ca', 'ie', 'gb', 'au', 'nz'] # https://newsdata.io/news-sources
    language = 'en'

    # Loop over countries
    for country_code in country_codes:
        # Fetch the news
        response = client.news_api(
            country=country_code,
            language=language,
            max_result=max_result
        )

        # Process the response
        if 'status' in response and response['status'] == 'success':
            articles = response['results']
            # Process the articles as needed
            for article in articles:
                all_articles.append(article)
        else:
            print("Failed to retrieve data:", response.get('message', 'Unknown Error'))
    # Put all the articles in a dataframe
    df_news = pd.DataFrame(all_articles)

    return df_news


def set_date_format(df: pd.DataFrame) -> pd.DataFrame:
    """Reformat date such that the time is dropped and just the date is kept

    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        df (pd.DataFrame): Output dataframe with the publication date set to datetime
    """
    df['pubDate'] = pd.to_datetime(df['pubDate'])
    return df


def set_string_columns(df: pd.DataFrame, cat_columns: list[str]) -> pd.DataFrame:
    """Set the categorical columns to string types

    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        df (pd.DataFrame): Output dataframe
    """
    for feat in cat_columns:
        df[feat] = df[feat].astype(str)
    return df


def drop_unavailable_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Drop unavailable columns when not using the paid version of NewsDataAPI

    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        (pd.DataFrame): Output dataframe
    """
    return df.drop(columns=[
        "content", "ai_tag", "sentiment",
       "sentiment_stats", "ai_region", "ai_org",
    ])


def login_to_feature_store():
    """
    """
    project = hopsworks.login()
    return project.get_feature_store()


def send_data_to_feature_store(fs, df: pd.DataFrame, version: int) -> None:
    """
    """
    # Put articles in feature store
    fs_news = fs.get_or_create_feature_group(
        name="news_articles",
        version=version,
        primary_key=['article_id'],
        description="News articles dataset"
    )
    fs_news.insert(df)
