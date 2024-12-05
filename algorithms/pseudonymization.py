"""
Hash-based pseudonymization methods.
"""

import hashlib
from typing import List
import pandas as pd

def pseudonymize_column(df: pd.DataFrame, column_name: str, salt: str = "") -> pd.DataFrame:
    """
    Applies pseudonymization to a specified column using hashing.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        column_name (str): Name of the column to pseudonymize.
        salt (str): Optional salt to add randomness to the hashing.

    Returns:
        pd.DataFrame: DataFrame with the column pseudonymized.
    """
    def hash_value(value):
        return hashlib.sha256(f"{value}{salt}".encode()).hexdigest()
    
    df[column_name] = df[column_name].astype(str).apply(hash_value)
    return df
