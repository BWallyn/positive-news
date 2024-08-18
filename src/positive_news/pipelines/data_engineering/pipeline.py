"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.19.7
"""

from kedro.pipeline import Pipeline, node, pipeline

from .nodes import (
    drop_unavailable_columns,
    drop_unnecessary_columns,
    rename_columns,
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
                func=drop_unnecessary_columns,
                inputs=["df_news_without_unavailable_cols", "params:data_engineering.cols_to_remove"],
                outputs="df_news_without_unnecessary_cols",
                name="remove_unnecessary_columns"
            ),
            node(
                func=set_date_format,
                inputs="df_news_without_unnecessary_cols",
                outputs="df_news_date_format",
                name="set_date_format"
            ),
            node(
                func=set_string_columns,
                inputs=["df_news_date_format", "params:data_engineering.cat_columns"],
                outputs="df_news_string_cols",
                name="set_string_columns_format"
            ),
            node(
                func=rename_columns,
                inputs="df_news_string_cols",
                outputs="df_news_cols_renamed",
                name="rename_column_names"
            )
        ],
        outputs="df_news_cols_renamed",
        namespace="data_engineering",
        parameters=["data_engineering.max_results", "data_engineering.cols_to_remove", "data_engineering.cat_columns"]
    )
