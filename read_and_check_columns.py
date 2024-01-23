import pandas as pd

def read_and_check_columns(file_path, expected_cols):
    try:
        goods_transaction = pd.read_excel(file_path)

        if not set(expected_cols).issubset(goods_transaction.columns):
            raise ValueError('The file does not contain the expected columns:', expected_cols)

    except Exception as e:
        print('Error:', e)
        goods_transaction = pd.DataFrame()  # Return an empty DataFrame in case of an error

    return goods_transaction
