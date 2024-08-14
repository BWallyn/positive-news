"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.7
"""
# =================
# ==== IMPORTS ====
# =================

import pandas as pd
from newsdataapi import NewsDataApiClient

# ===================
# ==== FUNCTIONS ====
# ===================

def request_news(api_key: str) -> pd.DataFrame:
    """
    """
    # Create a NewsData API client
    client = NewsDataApiClient(apikey=api_key)

    # Collect articles from many countries in a list
    all_articles = []
    country_codes = ['us', 'ca', 'ie', 'gb', 'au', 'nz'] # https://newsdata.io/news-sources
    language = 'en'

    # Loop over countries
    for country_code in country_codes:
        # Fetch the news
        response = client.news_api(country=country_code, language=language)

        # Process the response
        if 'status' in response and response['status'] == 'success':
            articles = response['results']
            # Process the articles as needed
            for article in articles:
                all_articles.append(article)
        else:
            print("Failed to retrieve data:", response.get('message', 'Unknown Error'))
    # Put all the articles in a dataframe
    news_df = pd.DataFrame(all_articles)

    return news_df
