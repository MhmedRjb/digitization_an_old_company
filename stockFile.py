import pandas as pd
import numpy as np
from UtilityFunctions import fill_non_blank_down, codetoname, add_left_zero, slice_barcode

def stockFile(file_path):

    all_item = pd.read_excel(r"D:\result\FILES\New folder (2)\Sbitmsmfrpt_ORG.xls")
    item_with_det = pd.read_excel(r"C:\Users\mohamed\Desktop\item_with_det.xlsx")
    all_item = all_item.dropna(subset=['itm_cd']).reset_index(drop=True)
    item_with_det = item_with_det.dropna(subset=['itm_cd']).reset_index(drop=True)

    add_left_zero(all_item, 'itm_cd')
    add_left_zero(item_with_det, 'itm_cd')

    slice_barcode(item_with_det,[0,2,0] , 'itm_cd')
    slice_barcode(item_with_det,[0, 4, 1], 'itm_cd')

    codetoname(item_with_det, all_item, 'itm_cd','ITM_NM', 'itm_cd_T1')
    codetoname(item_with_det, all_item, 'itm_cd','ITM_NM', 'itm_cd_T2')

    # Read the Excel file
    store = pd.read_excel(file_path)

    # Clean the 'itm_cd' column
    store['itm_cd'] = store['itm_cd'].replace(r'[^0-9]', np.nan, regex=True).reset_index(drop=True)

    # Drop unnecessary column
    store = store.drop('Text25', axis=1)

    # Rename columns for better readability
    store.rename(columns={
        'sBal': 'الرصيد عدد',
        'sOutQty': 'الصادر عدد',
        'sInQty': 'الوارد عدد',
        'sLbl': 'اخر جرد عدد',
        'نص98': 'اخر جرد وزن',
        'نص97': 'الرصيد وزن',
        'نص96': 'الصادر وزن',
        'نص95': 'الوارد وزن',
        'Text77': 'المخزن',
    }, inplace=True)

    # Fill non-blank values down for 'ITM_NM' and 'itm_cd' columns
    fill_non_blank_down(store, 'ITM_NM')
    fill_non_blank_down(store, 'itm_cd')

    return store, item_with_det


