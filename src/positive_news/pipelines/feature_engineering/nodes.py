"""
This is a boilerplate pipeline 'feature_engineering'
generated using Kedro 0.19.7
"""
# =================
# ==== IMPORTS ====
# =================

import pandas as pd

# ===================
# ==== FUNCTIONS ====
# ===================

def prepare_data_for_hf(df: pd.DataFrame) -> pd.DataFrame:
    """Prepare dataframe for HuggingFace datasets

    Args:
        df (pd.DataFrame): Input dataframe
    Returns:
        (pd.DataFrame): Output dataframe with just the needed columns
    """
    df = df.rename(columns={
        "title": "text",
        "sentiment": "label"
    })
    if "label" in df.columns:
        return df[["text", "label"]]
    else:
        return df[["text"]]
