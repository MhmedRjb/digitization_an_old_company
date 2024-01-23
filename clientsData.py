import pandas as pd
import numpy as np
from UtilityFunctions import  codetoname, slice_barcode

def clientsData(file_path):
    clints_df = pd.read_excel(file_path)
    clints_df = clints_df.replace(r'^\s*$', np.nan, regex=True)
    clints_df.drop(clints_df.index[clints_df['acc_nm'].isnull()], inplace=True)

    clints_df['acc_cd'] = clints_df['acc_cd'].astype('int32').astype('str')
    clints_df = clints_df.reset_index()

    clints_df = clints_df[(clints_df['acc_nm'].str.contains(
        '^(?!فروع).*$')) & (clints_df['acc_cd'].str.contains('.2.....{0,2}$'))].reset_index(drop=True)

    slice_barcode(clints_df, [0, 3, 0],'minat1' )
    slice_barcode(clints_df, 'minat2',,[ 0, 4, 1])
    slice_barcode(clints_df, [0, 6, 2],'minat3')

    codetoname(clints_df, clints_df, 'acc_cd','acc_nm', 'minat1')
    codetoname(clints_df, clints_df, 'acc_cd','acc_nm', 'minat2')
    codetoname(clints_df, clints_df, 'acc_cd','acc_nm', 'minat3')
    clints_df['minat3_name'] = clints_df['minat3_name'].fillna(clints_df['minat2_name'])
    clints_df['minat2_name'] = clints_df['minat2_name'].fillna(clints_df['minat1_name'])

    # todo"make somthing in data base it selfe "
    clints_df['tax'] = np.where(clints_df['minat3'].astype(str).str.contains('123101.*'), 0.08,
                                       np.where(clints_df['minat3'].astype(str).str.contains('123104.*'), 0.04,
                                                np.where(clints_df['minat3'].astype(str).str.contains('12310[2,3].*'), 0.01,
                                                         0.00)))
    return clints_df




