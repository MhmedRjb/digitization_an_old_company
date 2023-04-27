import pandas as pd
import numpy as np


import pandas as pd

def give_value_for_each(df, col_name,df2,condition_col, condition):

    df[col_name] = df.apply(lambda row: print(df2[row.name]) or df2[row.name] if row[condition_col] == condition else '', axis=1)
    return df


df1df = pd.DataFrame({'Gender': ['Male', 'Male', 'Female', 'Male', 'Female','Male', 'Male', 'Female','Female','Female','Female','Female','Female','Female','Female','Female','Female', 'Male', 'Female','Male','Male','Male','Male','Male','Male','Male','Male']
                   ,'Age':  [1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]})
print(df1df)
mask_names = ['Mask a', 'Mask b2', 'Mask d3', 'Mask 4', 'Mask 5','Mask 6', 'Mask 7', 'Mask 8', 'Mask 9', 'Mask 10','Mask 11', 'Mask sss12', 'Mask 13', 'Mask 14', 'Mask 15','Mask 16', 'Mask 17' ]
mask_index = 0
male_rows = df1df['Gender'] == 'Male'
df1df.loc[male_rows, 'Mask'] = mask_names[:sum(male_rows)]

print(df1df)


clints_df = pd.read_excel(r"D:\result\FILES\New folder (2)\SBAccMFDtlRpt.xls")
clints_df = clints_df.replace(r'^\s*$', np.nan, regex=True)
clints_df.drop(clints_df.index[clints_df['acc_nm'].isnull()], inplace=True)

clints_df['acc_cd'] = clints_df['acc_cd'].astype('int32').astype('str')
clints_df = clints_df.reset_index()



#############################

clints_df.columns = ['index', 'empty1', 'empty2', 'code', 'acc_nm', 'mony_forus', 'mony_onus', 'place', 'empty3', 'empty4', 'empty5',
                     'empty5', "man", "max_mony", "max_time"]

clints_df["max_time"] = clints_df["max_time"].astype("int32")



acc_stat = pd.read_excel(r"D:\result\FILES\New folder (2)\SBACCRPTA4.xls")
acc_stat.drop(['Text139', 'نص204'], axis=1,inplace=True)
clints_df['acc_nm'] = clints_df['acc_nm'].fillna(0).reset_index(drop=True)

clints_df=clints_df['acc_nm']

male_rows = acc_stat['TR_DS'] == 'ماقبله'
print(male_rows.head(40))
acc_stat.loc[male_rows, 'Mask'] = clints_df[:sum(male_rows)]
print(acc_stat.head(40))

"""
def assign_names_by_value(df, column, value, names):

    Assigns a name to each row in the input DataFrame where the value in the specified column matches the specified value.

    This function takes a DataFrame, a column name, a value, and a list of names as input. It checks if the number of names is exactly equal to the number of rows in the DataFrame where the value in the specified column matches the specified value and raises an error if these numbers are not equal. If the numbers are equal, the function assigns a name from the names list to each matching row in the DataFrame.

    :param df: A DataFrame containing data on individuals.
    :param column: The name of the column to check for matching values.
    :param value: The value to match in the specified column.
    :param names: A list of names to assign to matching rows in the input DataFrame.
    :return: A new DataFrame with an additional 'Name' column containing the assigned names.
    :raises ValueError: If the number of names does not match the number of matching rows in the input DataFrame.
  
    matching_rows = df[column] == value
    num_matching_rows = sum(matching_rows)
    if num_matching_rows != len(names):
        raise ValueError(f'The number of names ({len(names)}) does not match the number of matching rows ({num_matching_rows})')
    result_df = df.copy()
    result_df.loc[matching_rows, 'Name'] = names[:sum(matching_rows)]
    return result_df

print (assign_names_by_value(acc_stat, 'TR_DS', 'ماقبله', clints_df))

def assign_names_by_value2(target_df, condition_column, condition_value, names_df,clo_name,col_name):
    
    Assigns a name to each row in the input DataFrame where the value in the specified column matches the specified value.

    This function takes a DataFrame, a column name, a value, and a list of names as input. It checks if the number of names is exactly equal to the number of rows in the DataFrame where the value in the specified column matches the specified value and raises an error if these numbers are not equal. If the numbers are equal, the function assigns a name from the names list to each matching row in the DataFrame.

    :param df: A DataFrame containing data on individuals.
    :param condition_column: The name of the column to check for matching values.
    :param value: The value to match in the specified column.
    :param names: A list of names to assign to matching rows in the input DataFrame.
    :return: A new DataFrame with an additional 'Name' column containing the assigned names.
    :raises ValueError: If the number of names does not match the number of matching rows in the input DataFrame.
   
    
    # Use pandas built-in methods to filter and assign values
    target_df[col_name] = pd.NA # Create a new column with missing values
    target_df.loc[target_df[condition_column] == condition_value, col_name] = names_df[clo_name] # Assign names to matching rows
    
    # Check if the number of names matches
    if len(target_df[target_df[condition_column] == condition_value]) != len(names_df):
        raise ValueError(f'The number of names ({len(names_df)}) does not match the number of matching rows ({len(target_df[target_df[condition_column] == condition_value])})')
    
    # Return a new DataFrame with all columns and rows
    return target_df
assign_names_by_value2(acc_stat, 'TR_DS', 'ماقبله', clints_df,'acc_nm','acc_nm')
print(acc_stat)

"""