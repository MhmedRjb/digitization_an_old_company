import pandas as pd
from UtilityFunctions import preprocess_and_slice,fill_non_blank_down,codetoname,read_and_check_columns

def clean_and_rename_columns(budget):
    budget.drop(budget.columns[:14], axis=1, inplace=True)
    new_column_names = {'DbBal': 'الحركة مدين',
                        'CrBal': 'الحركة دائن',
                        'Label113': 'مدين نهاية المدة',
                        'Text153': 'مدين أول المدة',
                        'Text154': 'دائن أول المدة',
                        'Text161': 'دائن اخر المدة'}
    budget.rename(columns=new_column_names, inplace=True)
    return budget

def accountjournal(file_path, expected_cols):
    # Define the list of expected column names should be exist in the file
    expected_columns = ['Acc_cd', 'cboHdr2', 'cboHdrNo2']

    # Specify the file path for accountjournal
    account_journal_path = r"path_to_accountjournal\accountjournal.xlsx"  # Replace with the actual path

    # Read and check the accountjournal file
    account_journal = read_and_check_columns(account_journal_path, expected_columns)

    # Print accountjournal for verification
    print("Account Journal File:")
    print(account_journal)

    # Specify the file path for the budget file
    budget_path = r"D:\result\FILES\New folder (2)\SBaccTriRpt.xls"

    # Read and check the budget file
    budget = read_and_check_columns(budget_path, expected_columns)

    # Preprocess the budget DataFrame and slice barcode
    slices = [(0, 1, 'minat1', 0), 
              (0, 2, 'minat2', 1),
              (0, 3, 'minat3', 2),
              (0, 4, 'minat4', 3),
              (0, 5, 'minat5', 4),
              (0, 6, 'minat6', 5),
              (0, 7, 'minat7', 6),
              (0, 8, 'minat8', 7),
              (0, 9, 'minat9', 8)]
    budget = preprocess_and_slice(budget, 'Acc_cd', slices)

    # Map the code values to the corresponding names in the budget DataFrame
    cols_to_map = ['minat1', 'minat2', 'minat3', 'minat5', 'minat6', 'minat8']
    budget = codetoname(budget, account_journal, 'Acc_cd', 'Acc_nm', cols_to_map)

    # Fill non-blank down in specified columns
    non_blank_columns = ['minat1_name', 'minat2_name', 'minat3_name', 'minat5_name', 'minat6_name', 'minat8_name']
    budget = fill_non_blank_down(budget, non_blank_columns)

    # Clean and rename columns
    budget = clean_and_rename_columns(budget)
    return budget

