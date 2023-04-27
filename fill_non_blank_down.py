def fill_non_blank_down(df, column):
    """
    Fill NaN values in the specified column with the previous non-NaN value in the same column.
    """
    df[column] = df[column].fillna(method='bfill')
    df[column] = df[column].fillna(method='ffill')
    return df
import pandas as pd

def fill_non_blank_down2(df, column):
    previous_value = 0
    for i in range(1, df.shape[0]):
        if pd.isna(df.loc[i, column]) is False:
            previous_value = df.loc[i, column]
        else:
            df.loc[i, column] = previous_value
    return df