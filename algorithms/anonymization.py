"""
Functions for k-anonymity, l-diversity, and t-closeness.
"""

import pandas as pd
import numpy as np
from typing import List, Union

def apply_k_anonymity(
    df: pd.DataFrame, 
    quasi_identifiers: List[str], 
    k: int
) -> pd.DataFrame:
    """
    Applies k-anonymity to the given DataFrame by grouping rows based on quasi-identifiers.
    
    Args:
        df (pd.DataFrame): Input DataFrame to anonymize.
        quasi_identifiers (List[str]): Columns that act as quasi-identifiers.
        k (int): Minimum group size for k-anonymity.

    Returns:
        pd.DataFrame: Anonymized DataFrame.
    """
    grouped = df.groupby(quasi_identifiers)
    valid_groups = [name for name, group in grouped if len(group) >= k]
    
    anonymized_df = pd.concat([grouped.get_group(name) for name in valid_groups], ignore_index=True)
    return anonymized_df.reset_index(drop=True)

def apply_l_diversity(
    df: pd.DataFrame, 
    quasi_identifiers: List[str], 
    sensitive_column: str, 
    l: int
) -> pd.DataFrame:
    """
    Applies l-diversity by ensuring each group of quasi-identifiers contains at least `l` diverse sensitive values.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        quasi_identifiers (List[str]): Columns that act as quasi-identifiers.
        sensitive_column (str): Sensitive attribute to evaluate diversity.
        l (int): Minimum diversity of sensitive values within each group.

    Returns:
        pd.DataFrame: Anonymized DataFrame with l-diversity applied.
    """
    grouped = df.groupby(quasi_identifiers)
    valid_groups = [
        name for name, group in grouped 
        if group[sensitive_column].nunique() >= l
    ]
    
    anonymized_df = pd.concat([grouped.get_group(name) for name in valid_groups], ignore_index=True)
    return anonymized_df.reset_index(drop=True)

def apply_t_closeness(
    df: pd.DataFrame, 
    quasi_identifiers: List[str], 
    sensitive_column: str, 
    t: float
) -> pd.DataFrame:
    """
    Applies t-closeness by ensuring the distribution of a sensitive attribute within each group is close to the overall distribution.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
        quasi_identifiers (List[str]): Columns that act as quasi-identifiers.
        sensitive_column (str): Sensitive attribute to evaluate distribution.
        t (float): Threshold for distribution closeness.

    Returns:
        pd.DataFrame: Anonymized DataFrame with t-closeness applied.
    """
    overall_distribution = df[sensitive_column].value_counts(normalize=True)
    
    def is_t_close(group):
        group_distribution = group[sensitive_column].value_counts(normalize=True)
        divergence = (group_distribution - overall_distribution).abs().sum()
        return divergence <= t

    grouped = df.groupby(quasi_identifiers)
    valid_groups = [
        name for name, group in grouped 
        if is_t_close(group)
    ]
    
    anonymized_df = pd.concat([grouped.get_group(name) for name in valid_groups], ignore_index=True)
    return anonymized_df.reset_index(drop=True)
