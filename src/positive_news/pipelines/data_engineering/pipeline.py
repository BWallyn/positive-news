"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    drop_unavailable_columns,
    request_news,
    set_date_format,
    set_string_columns,
)


def create_pipeline(**kwargs) -> Pipeline:
    return pipeline(
        [
            node(
                func=request_news,
                inputs=["credentials:news_data_api_key", "params:data_engineering.max_results"],
                outputs="df_news",
                name="request_news_NewsDataAPI"
            ),
            node(
                func=drop_unavailable_columns,
                inputs="df_news",
                outputs="df_news_without_unavailable_cols",
                name="remove_unavailable_columns"
            ),
            node(
                func=set_date_format,
                inputs="df_news_without_unavailable_cols",
                outputs="df_news_date_format",
                name="set_date_format"
            ),
            node(
                func=set_string_columns,
                inputs=["df_news_date_format", "params:data_engineering.cat_columns"],
                outputs="df_news_string_cols",
                name="set_string_columns_format"
            )
        ],
        outputs="df_news_string_cols"
    )
