from transectionFile import transectionFile
from UtilityFunctions import read_and_check_columns
from accountjournal import accountjournal
from clientsData import clientsData
from stockFile import stockFile
from CashFlowData import CashFlowData
import pandas as pd

file_path_transectionFile = "D:\result\FILES\New folder (2)\SBAcc.xls"  # Replace with your actual file path
expected_cols_transectionFile = ['Acc_Nm', 'sCst', 'Text103', 'Text120', 'Text101', 'sPrc', 'sQty', 'spkid']

# Call the main function
buying_df, selling_df, goods_movements_df = transectionFile(file_path_transectionFile, expected_cols_transectionFile)

expected_columns_accountjournal = ['Acc_cd', 'cboHdr2', 'cboHdrNo2']
file_path_accountjournal = r"path_to_accountjournal\accountjournal.xlsx"  # Replace with the actual path
budget_df=accountjournal(file_path_accountjournal, expected_columns_accountjournal)

file_bath_stockFile=r"D:\result\FILES\New folder (2)\SBINQALLRPT_CTRL.xls"  
stock_df,item_df=stockFile(file_bath_stockFile)
file_bath_clints=r"D:\result\FILES\New folder (2)\SBaccmfrpt_BRF.xls"
clints_df=clientsData(file_bath_clints)
CashFlowData_df=CashFlowData(clints_df,budget_df,selling_df)


with pd.ExcelWriter(r"D:\result\result.xlsx", engine="openpyxl") as writer:
    buying_df.to_excel(writer, sheet_name='buying_df')
    selling_df.to_excel(writer, sheet_name='selling_df')
    goods_movements_df.to_excel(writer, sheet_name='goods_movements_df')
    budget_df.to_excel(writer, sheet_name='budget_df')
    stock_df.to_excel(writer, sheet_name='stock_df')
    item_df.to_excel(writer, sheet_name='item_df')
    clints_df.to_excel(writer, sheet_name='clints_df')
    CashFlowData_df.to_excel(writer, sheet_name='CashFlowData_df')



