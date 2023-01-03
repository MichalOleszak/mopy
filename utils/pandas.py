import numpy as np
import pandas as pd


def optimize_df_memory_usage(df, perc_unique_categories=0.5):
    """
    Reduce the memory usage of a pandas Data.Frame by downcasting and converting dtypes.
    Based on this blog post: https://www.dataquest.io/blog/pandas-big-data/.
    :param df: A pandas Data.Frame.
    :param perc_unique_categories: A float in <0., 1.> denoting the threshold for the percentage
    of category values that are unique; variables with this percentage higher than threshold
    will not be converted to categorical type.
    :return: A pandas Data.Frame with reduced memory usage.
    """
    converted_int = df.select_dtypes(include=["int"]).apply(pd.to_numeric, downcast="integer")
    converted_float = df.select_dtypes(include=["float"]).apply(pd.to_numeric, downcast="float")

    df_obj = df.select_dtypes(include=["object"]).copy()
    converted_obj = pd.DataFrame()
    for col in df_obj.columns:
        num_unique_values = len(df_obj[col].unique())
        num_total_values = len(df_obj[col])
        if num_unique_values / num_total_values < perc_unique_categories:
            converted_obj.loc[:, col] = df_obj[col].astype("category")
        else:
            converted_obj.loc[:, col] = df_obj[col]

    df[converted_int.columns] = converted_int
    df[converted_float.columns] = converted_float
    df[converted_obj.columns] = converted_obj

    return df


def concat_with_categoricals(df_list):
    """
    Concatenate data frames while preserving categorical variables' type.
    Based on this StackOvereflow thread:
    https://stackoverflow.com/questions/45639350/retaining-categorical-dtype-upon-dataframe-concatenation
    :param df_list: A list of pandas Data.Frames
    :return: A concatenated pandas Data.Frame with categorical variables.
    """
    for col in set.intersection(*[set(df.select_dtypes(include="category").columns) for df in df_list]):
        uc = pd.api.types.union_categoricals([df[col] for df in df_list])
        for df in df_list:
            df[col] = pd.Categorical(np.asarray(df[col]), categories=uc.categories)

    return pd.concat(df_list, sort=False).reset_index(drop=True)
