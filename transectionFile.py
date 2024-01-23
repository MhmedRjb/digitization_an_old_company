import pandas as pd
import numpy as np
from UtilityFunctions import read_and_check_columns

# Function to clean column names and drop NaN columns
def clean_columns(goods_transaction):
    goods_transaction = goods_transaction.dropna(axis='columns', how="all")
    goods_transaction.columns = ['Inv_No', 'Inv', 'acc_name', 'cost', 'value', 'tax', 'discount', 'unitprice',
                                'quantity', 'type', 'invoice_type', 'item_NAME', 'ITEM_CODE', 'INVOICE_T1', 'INVOICE', 'DATE']
    return goods_transaction

# Function to filter and process buying transactions
def process_buying(goods_transaction):
    buying_df = goods_transaction[(goods_transaction['invoice_type'].str.contains('مرتد|شراء'))].reset_index(drop=True)
    buying_df['buying_total'] = np.where(buying_df['invoice_type'].str.contains('شراء'), buying_df['cost'], -buying_df['value'])
    buying_df['quantity_total'] = np.where(buying_df['invoice_type'].str.contains('شراء'), buying_df['quantity'], -buying_df['quantity'])
    return buying_df

# Function to filter and process selling transactions
def process_selling(goods_transaction):
    selling_df = goods_transaction[(goods_transaction['invoice_type'].str.contains('مرتجع|بيع'))].reset_index(drop=True)
    selling_df['gross_profit'] = np.where((selling_df['invoice_type'].str.contains('بيع')), selling_df['value'] - selling_df['cost'], -(selling_df['value'] - selling_df['cost']))
    selling_df['gross_sell'] = np.where((selling_df['invoice_type'].str.contains('بيع')), selling_df['value'], -(selling_df['value']))
    selling_df['total_quantity'] = np.where((selling_df['invoice_type'].str.contains('بيع')), selling_df['quantity'], -(selling_df['quantity']))
    selling_df = selling_df.drop(['tax'], axis=1).reset_index(drop=True)
    return selling_df

# Function to filter and process goods movements transactions
def process_goods_movements(goods_transaction):
    goods_movements_df = goods_transaction[(goods_transaction['invoice_type'].str.contains('ت.خصم|ت.إضافه|تحويل له|تحويل منه'))].reset_index(drop=True)
    goods_movements_df.rename(columns={'acc_name': 'store'}, inplace=True)
    return goods_movements_df

# Main function that orchestrates the entire process
def transectionFile(file_path, expected_cols):
    goods_transaction = read_and_check_columns(file_path, expected_cols)

    if not goods_transaction.empty:
        goods_transaction = clean_columns(goods_transaction)

        buying_df = process_buying(goods_transaction)
        selling_df = process_selling(goods_transaction)
        goods_movements_df = process_goods_movements(goods_transaction)

        return buying_df, selling_df, goods_movements_df
    else:
        print("Error occurred during file reading or processing.")
        raise ValueError("Error occurred. Returning empty DataFrames.")

    # Return empty DataFrames outside the else block