import pandas as pd

clints_file_an_ordianty = pd.read_excel(r"D:\SBJRNLITMRPTTAXCLINTS.xls")
non_clints_file_an_ordianty = pd.read_excel(r"D:\SBJRNLITMRPTTAXWITHOUTCLNYD.xls")
print(clints_file_an_ordianty.shape)
print(non_clints_file_an_ordianty.shape)

def assign_names_by_value(df: pd.DataFrame, column: str, value: Any, names: List[str]) -> pd.DataFrame:
    """
    Assigns a name to each row in the input DataFrame where the value in the specified column matches the specified value.

    This function takes a DataFrame, a column name, a value, and a list of names as input. It checks if the number of names is exactly equal to the number of rows in the DataFrame where the value in the specified column matches the specified value and raises an error if these numbers are not equal. If the numbers are equal, the function assigns a name from the names list to each matching row in the DataFrame.

    :param df: A DataFrame containing data on individuals.
    :param column: The name of the column to check for matching values.
    :param value: The value to match in the specified column.
    :param names: A list of names to assign to matching rows in the input DataFrame.
    :return: A new DataFrame with an additional 'Name' column containing the assigned names.
    :raises ValueError: If the number of names does not match the number of matching rows in the input DataFrame.
    """
    matching_rows = df[column] == value
    num_matching_rows = sum(matching_rows)
    if num_matching_rows != len(names):
        raise ValueError(f'The number of names ({len(names)}) does not match the number of matching rows ({num_matching_rows})')
    result_df = df.copy()
    result_df.loc[matching_rows, 'Name'] = names
    return result_df

