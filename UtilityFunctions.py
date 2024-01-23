import pandas as pd
import numpy as np

def read_and_check_columns(file_path, expected_cols):
    try:
        goods_transaction = pd.read_excel(file_path)

        if not set(expected_cols).issubset(goods_transaction.columns):
            raise ValueError('The file does not contain the expected columns:', expected_cols)

    except Exception as e:
        print('Error:', e)
        goods_transaction = pd.DataFrame()  # Return an empty DataFrame in case of an error

    return goods_transaction



def preprocess_and_slice(budget, code_col, slice_list):
    budget[code_col] = '0' + budget[code_col].astype('int32').astype('str')
    for start, end, col_name, position in slice_list:
        budget.insert(position, col_name, budget[code_col].astype(str).str.slice(start, end))
    return budget

def fill_non_blank_down(df, columns):
    for col in columns:
        df[col].fillna(method='ffill', inplace=True)
    return df

def codetoname(df, mapping_df, code_col, name_col, cols_to_map):
    translator = mapping_df.set_index(code_col)[name_col].to_dict()
    for col in cols_to_map:
        df[f'{col}_name'] = df[col].map(translator)
    return df


def give_name_for_NAN_in_another_col(traget_df, badeling_col, badeling_value, changabel_col, insert_df, insert_value):
    j = -1
    for i in range(0, traget_df.shape[0]):
        if traget_df.loc[i, badeling_col] == badeling_value:
            j = j + 1
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]
        else:
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]

def slice_barcode(df, slice_list, column_to_slice):
    for start, end, col_name, position in slice_list:
        df[col_name] = df[column_to_slice].astype(str).str.slice(start, end)
        col = df.pop(col_name)
        df.insert(position, col.name, col)
    return df
