"""
Noise addition for differential privacy.
"""

import numpy as np
import pandas as pd

def add_laplace_noise(
    df: pd.DataFrame, 
    column_name: str, 
    epsilon: float, 
    sensitivity: float
) -> pd.DataFrame:
    """
    Adds Laplace noise to a numeric column for differential privacy.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        column_name (str): Column to which noise is added.
        epsilon (float): Privacy budget parameter (higher = less noise).
        sensitivity (float): Sensitivity of the column's data.

    Returns:
        pd.DataFrame: DataFrame with noise added to the specified column.
    """
    noise = np.random.laplace(0, sensitivity / epsilon, size=len(df))
    df[column_name] += noise
    return df
