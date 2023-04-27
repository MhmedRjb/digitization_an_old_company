import numpy as np
import pandas as pd
import timeit

start_time = timeit.default_timer()

# Your code here



def add_left_zero(df, codel_col):
    df[codel_col] = '0' + df[codel_col].astype('int32').astype('str')


def slice_barcode(df, new_column, thebarcode, frist_postion, last_postion, postion=0):

    df[new_column] = df[thebarcode].astype(str).str[frist_postion:last_postion]
    col = df.pop(new_column)
    df.insert(postion, col.name, col)

def slice_barcode1(df, slice_list, column_to_slice):
    """
    Slices a column in a dataframe and inserts the resulting columns at specified positions.

    Args:
        df: A pandas dataframe.
        slice_list: A list of tuples specifying the start and end indices of the slices,
            the name of the resulting column, and the position to insert the column at.
        column_to_slice: The name of the column to slice.

    Returns:
        The modified dataframe.
    """
    for start, end, col_name, position in slice_list:
        df[col_name] = df[column_to_slice].astype(str).str.slice(start, end)
        col = df.pop(col_name)
        df.insert(position, col.name, col)
    return df

def fill_non_blank_down(df, column):
    """
    Fill NaN values in the specified column with the previous non-NaN value in the same column.

    Args:
        df: A pandas dataframe.
        column: The name of the column to fill.

    Returns:
        The modified dataframe.
    """

    df[column] = df[column].fillna(method='ffill')
    return df

def codetoname(target_df, translatr_df, DIC_KEY, DIC_value, traget_code_col, new_name_col, default_name=np.NAN):
    """
    Map codes to names in a pandas dataframe using a translation table.

    Args:
        target_df (pandas.DataFrame): The dataframe containing the code values to be mapped to names.
        translatr_df (pandas.DataFrame): The dataframe containing the translation table mapping codes to names.
        DIC_KEY (str): The name of the column in the `translatr_df` dataframe that contains the code values.
        DIC_value (str): The name of the column in the `translatr_df` dataframe that contains the corresponding names.
        traget_code_col (str): The name of the column in the `target_df` dataframe that contains the code values to be mapped.
        new_name_col (str): The name of the new column to be added to the `target_df` dataframe that will contain the corresponding names.
        default_name (str, optional): The default name to use for codes that are not found in the translation table. Defaults to "UNKNOWN".

    Raises:
        KeyError: If a code value is not found in the translation table.

    Returns:
        pandas.DataFrame: The modified `target_df` dataframe with the new `new_name_col` column.
    """

    # Create a dictionary to map codes to names
    translator = {row[DIC_KEY]: row[DIC_value] for _, row in translatr_df.iterrows()}
    
    # Map the values in the traget_code_col column to their corresponding names using the translator dictionary
    try:
        target_df[new_name_col] = target_df[traget_code_col].map(translator)
    except KeyError as ex:
        raise KeyError(f"Error: Code {ex} not found in translation table.") from ex
    
    # Handle missing names by filling NaN values with a default name
    target_df[new_name_col].fillna(default_name, inplace=True)
    
    return target_df

def codetoname2(df, mapping_df, code_col, name_col, cols_to_map):
    """
    Maps values in multiple columns from codes to names using a mapping table.

    Args:
        df (pandas.DataFrame): The dataframe to modify.
        mapping_df (pandas.DataFrame): The dataframe containing the mapping table for the codes.
        code_col (str): The name of the column containing the codes to map.
        name_col (str): The name of the column containing the corresponding names in the mapping table.
        cols_to_map (list): A list of column names to map from codes to names.

    Returns:
        pandas.DataFrame: The modified dataframe with new columns containing the mapped names.
    """
    translator = mapping_df.set_index(code_col)[name_col].to_dict()
    for col in cols_to_map:
        new_col_name = f'{col}_name'
        df[new_col_name] = df[col].map(translator)
    return df


##############################
expected_cols=['Acc_Nm','sCst',
               'Text103','Text120',
               'Text101','sPrc',
               'sQty',	'spkid']
try:
    goods_transection = pd.read_excel(r"D:\result\FILES\New folder (2)\SBJRNLITMRPTTAX.xls")
    if not set(expected_cols).issubset(goods_transection.columns):
        raise ValueError('The file does not contain the expected columns:', expected_cols)
except Exception as e:
    print('Error:', e)

goods_transection = goods_transection.dropna(axis='columns', how="all")
goods_transection.columns = ['Inv_No', 'Inv', 'acc_name', 'cost',
                'value', 'tax', 'discount', 'unitprice',
                'quantity', 'type', 'invoive_type',
                'item_NAME', 'ITEM_CODE', 'INVOICE_T1', 'INVOICE', 'DATE']
"filter the data"
buying_df = goods_transection[(goods_transection['invoive_type'].str.contains(
    'مرتد|شراء'))].reset_index(drop=True)

buying_df['buying_total'] = np.where(buying_df['invoive_type'].str.contains(
    'شراء'), buying_df['cost'], -buying_df['value'])

buying_df['quantity_total'] = np.where(buying_df['invoive_type'].str.contains(
    'شراء'), buying_df['quantity'], -buying_df['quantity'])

selling_df = goods_transection[(goods_transection['invoive_type'].str.contains(
    'مرتجع|بيع'))].reset_index(drop=True)

"get what you need from the data"
selling_df['gross_profit'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), selling_df['value'] - selling_df['cost'], -(selling_df['value'] - selling_df['cost']))

selling_df['gross_sell'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), selling_df['value'], -(selling_df['value']))

selling_df['total_quantity'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), selling_df['quantity'], -(selling_df['quantity']))

selling_df = selling_df.drop(['tax'], axis=1).reset_index(drop=True)

goods_movements_df = goods_transection[(goods_transection['invoive_type'].str.contains(
    'ت.خصم|ت.إضافه|تحويل له|تحويل منه'))].reset_index(drop=True)
goods_movements_df.rename(columns={'acc_name': 'store'}, inplace=True)

##############################

clints_df = pd.read_excel(r"D:\result\FILES\New folder (2)\SBAccMFDtlRpt.xls")
clints_df = clints_df.replace(r'^\s*$', np.nan, regex=True)
clints_df.drop(clints_df.index[clints_df['acc_nm'].isnull()], inplace=True)

clints_df['acc_cd'] = clints_df['acc_cd'].astype('int32').astype('str')
clints_df = clints_df.reset_index()

main_clint_df_t4 = clints_df[(clints_df['acc_nm'].str.contains(
    '^(?!فروع).*$')) & (clints_df['acc_cd'].str.contains('.2.....{0,2}$'))].reset_index(drop=True)


slice_barcode(main_clint_df_t4, 'minat1', 'acc_cd', 0, 3, 0)
slice_barcode(main_clint_df_t4, 'minat2', 'acc_cd', 0, 4, 1)
slice_barcode(main_clint_df_t4, 'minat3', 'acc_cd', 0, 6, 2)
codetoname(main_clint_df_t4, clints_df, 'acc_cd',
           'acc_nm', 'minat1', 'minat1_name')
codetoname(main_clint_df_t4, clints_df, 'acc_cd',
           'acc_nm', 'minat2', 'minat2_name')
codetoname(main_clint_df_t4, clints_df, 'acc_cd',
           'acc_nm', 'minat3', 'minat3_name')
main_clint_df_t4['minat3_name'] = main_clint_df_t4['minat3_name'].fillna(main_clint_df_t4['minat2_name'])
main_clint_df_t4['minat2_name'] = main_clint_df_t4['minat2_name'].fillna(main_clint_df_t4['minat1_name'])

# todo"make somthing in data base it selfe "
main_clint_df_t4['tax'] = np.where(main_clint_df_t4['minat3'].astype(str).str.contains('123101.*'), 0.08,
                                   np.where(main_clint_df_t4['minat3'].astype(str).str.contains('123104.*'), 0.04,
                                            np.where(main_clint_df_t4['minat3'].astype(str).str.contains('12310[2,3].*'), 0.01,
                                                     0.00)))

#############################

clints_df.columns = ['index', 'empty1', 'empty2', 'code', 'acc_nm', 'mony_forus', 'mony_onus', 'place', 'empty3', 'empty4', 'empty5',
                     'empty5', "man", "max_mony", "max_time"]

clints_df["max_time"] = clints_df["max_time"].astype("int32")


acc_stat = pd.read_excel(r"D:\result\FILES\New folder (2)\SBACCRPTA4.xls")
acc_stat.drop(['Text139', 'نص204'], axis=1,inplace=True)
clints_df['acc_nm'] = clints_df['acc_nm'].fillna(0)


def give_name_for_NAN_in_another_col(traget_df, badeling_col, badeling_value, changabel_col, insert_df, insert_value):
    j = -1
    for i in range(0, traget_df.shape[0]):
        if traget_df.loc[i, badeling_col] == badeling_value:
            j = j + 1
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]
        else:
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]


give_name_for_NAN_in_another_col(
    acc_stat, 'TR_DS', 'ماقبله', 'RACC', clints_df, 'acc_nm')




acc_stat['tr_dt'] = acc_stat['tr_dt'].replace(np.nan, "30/12/2022 00:00:00")

acc_stat['tr_dt'] = pd.to_datetime(acc_stat['tr_dt'], errors='coerce')

acc_stat["days"] = acc_stat["tr_dt"].dt.day

acc_stat = acc_stat.merge(clints_df, left_on='RACC',
                          right_on='acc_nm', how='left', suffixes=('_x', '_y'))

acc_stat = acc_stat.merge(main_clint_df_t4, left_on='RACC',
                          right_on='acc_nm', how='left', suffixes=('_x', '_y'))



def calculate_due_date(tr_date, payment_terms,TR_DS):
    if TR_DS.find("دائن") == 1 or TR_DS.find("مدين") == 1:
        return tr_date
    else:
        if payment_terms == 222:
            return tr_date.to_period('M').to_timestamp(how='end') + pd.Timedelta(15, unit='d')
        elif payment_terms == 333:
            if tr_date.day <= 15:
                return tr_date.to_period('M').to_timestamp(how='start') + pd.Timedelta(21, unit='d')
            else:
                return tr_date.to_period('M').to_timestamp(how='start') + pd.Timedelta(7, unit='d')
        elif payment_terms == 0:
            return tr_date
        elif payment_terms == 3:
            return tr_date + pd.Timedelta(3, unit='d')
        elif payment_terms == 15:
            return tr_date + pd.Timedelta(15, unit='d')
        elif payment_terms == 45:
            return tr_date + pd.Timedelta(45, unit='d')
        elif payment_terms == 565:
            if tr_date.day <= 21:
                return tr_date.to_period('M').to_timestamp(how='start') + pd.Timedelta(7, unit='d')
            else:
                return tr_date.to_period('M').to_timestamp(how='start') + pd.DateOffset(months=1) + pd.Timedelta(7, unit='d')
        else:
            raise ValueError('Unrecognized payment term: {}'.format(payment_terms))
#TODO: TEST THIS FUNCTION 
acc_stat['Libra'] = acc_stat.apply(lambda row: calculate_due_date(row['tr_dt'], row['max_time'],row['TR_DS']), axis=1)


acc_stat["mov_d"] = acc_stat["mov_d"].fillna(0)
acc_stat["mov_c"] = acc_stat["mov_c"].fillna(0)
acc_stat["Total_bal"] = -(acc_stat["mov_d"]-acc_stat["mov_c"])*(1-acc_stat["tax"])
lats_acc_stat = acc_stat[['RACC', 'tr_dt', "mov_d", "mov_c", "TR_DS", 'Libra', 'max_time',
                          'days', 'tax', 'Total_bal', 'bal_D', "bal_c", "TEXT207", "TEXT208", "Text184"]].copy(deep=False)

selling_df = pd.merge(main_clint_df_t4[['acc_nm', 'tax']], selling_df,
                     left_on='acc_nm', right_on='acc_name', how='right', validate='one_to_many')
selling_df = selling_df.drop(['acc_nm'], axis=1).reset_index(drop=True)

selling_df['net_sell'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), (selling_df['value']*(1-selling_df['tax'])), -(selling_df['value']*(1-selling_df['tax'])))

selling_df['net_profit'] = np.where((selling_df['invoive_type'].str.contains('بيع')), ((
    selling_df['value']*(1-selling_df['tax'])) - selling_df['cost']),
      -((selling_df['value']*(1-selling_df['tax'])) - selling_df['cost']))
selling_df['Profit Percentage(cost)'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), (selling_df['net_profit'] / selling_df['cost']), -(selling_df['net_profit'] / selling_df['cost']))
selling_df['Profit Percentage(value)'] = np.where((selling_df['invoive_type'].str.contains(
    'بيع')), (selling_df['net_profit'] / selling_df['value']), -(selling_df['net_profit'] / selling_df['value']))


helprt_acc = [lats_acc_stat['TR_DS'] .str.contains('مرتجع|بيع')]
helprt_acc = lats_acc_stat.groupby(['RACC', 'Libra', 'tr_dt'])[
    'Total_bal'].sum().reset_index()

sellhelper = acc_stat['tr_dt'].agg(['min', 'max'])
sellhelper["Days Elapsed"] = (
    sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'D')
sellhelper["Weeks Elapsed"] = (
    sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'W')
sellhelper["Months Elapsed"] = (
    sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'M')
sellhelper["Quarterly Intervals Elapsed"] = (
    sellhelper["max"] - sellhelper["min"]) / np.timedelta64(3, 'M')

#################################################################################################################


all_item = pd.read_excel(r"D:\result\FILES\New folder (2)\Sbitmsmfrpt_ORG.xls")
item_with_det = pd.read_excel(r"C:\Users\mohamed\Desktop\item_with_det.xlsx")
all_item = all_item.dropna(subset=['itm_cd']).reset_index(drop=True)
item_with_det = item_with_det.dropna(subset=['itm_cd']).reset_index(drop=True)

add_left_zero(all_item, 'itm_cd')
add_left_zero(item_with_det, 'itm_cd')

slice_barcode(item_with_det, 'itm_cd_T1', 'itm_cd', 0, 2, 0)
slice_barcode(item_with_det, 'itm_cd_T2', 'itm_cd', 0, 4, 1)

codetoname(item_with_det, all_item, 'itm_cd',
           'ITM_NM', 'itm_cd_T1', 'itm_cd_T1_name')
codetoname(item_with_det, all_item, 'itm_cd',
           'ITM_NM', 'itm_cd_T2', 'itm_cd_T2_name')

##############################


selling_df = selling_df.drop(['tax'], axis=1).reset_index(drop=True)

##############################

# Define the list of expected column names should be exist in the file
expected_cols = ['Acc_cd', 'cboHdr2', 'cboHdrNo2']

# Check if the expected columns are present in the file
'column should be exist in the file'
try:
    budget = pd.read_excel(r"D:\result\FILES\New folder (2)\SBaccTriRpt.xls")
    if not set(expected_cols).issubset(budget.columns):
        raise ValueError('The file does not contain the expected columns:', expected_cols)
except Exception as e:
    print('Error:', e)

# Clean and preprocess the budget DataFrame
budget = (
    budget
    .assign(Acc_cd=lambda x: x['Acc_cd'].replace(r'[^0-9]', np.nan, regex=True))
    .dropna(subset=['Acc_cd']).reset_index(drop=True)
    .astype({'Acc_cd': 'int32'})
    .astype({'Acc_cd': 'str'})
)

# Define the slice ranges for the barcode slicing function
slices = [(0, 1, 'minat1', 0), 
          (0, 2, 'minat2', 1),
          (0, 3, 'minat3', 2),
          (0, 4, 'minat4', 3),
          (0, 5, 'minat5', 4),
          (0, 6, 'minat6', 5),
          (0, 7, 'minat7', 6),
          (0, 8, 'minat8', 7),
          (0, 9, 'minat9', 8)]

# Slice the barcode values and replace them with the corresponding names
slice_barcode1(budget, slices, 'Acc_cd')

# Map the code values to the corresponding names in the budget DataFrame
cols_to_map = ['minat1', 'minat2', 'minat3', 'minat5', 'minat6', 'minat8']
codetoname2(budget, budget, 'Acc_cd', 'Acc_nm', cols_to_map)
fill_non_blank_down (budget,['minat1_name', 'minat2_name', 
                             'minat3_name', 'minat5_name', 
                             'minat6_name', 'minat8_name'])

# Drop columns with irrelevant indices
budget.drop(budget.columns[:14], axis=1, inplace=True)

# Rename remaining columns with more descriptive names
new_column_names = {'DbBal': 'الحركة مدين',
                    'CrBal': 'الحركة دائن',
                    'Label113': 'مدين نهاية المدة',
                    'Text153': 'مدين أول المدة',
                    'Text154': 'دائن أول المدة',
                    'Text161': 'دائن اخر المدة'}
budget.rename(columns=new_column_names, inplace=True)

#####################################################################################################################

store = pd.read_excel(r"D:\result\FILES\New folder (2)\SBINQALLRPT_CTRL.xls")

store['itm_cd'] = store['itm_cd'].replace(r'[^0-9]', np.nan, regex=True).reset_index(drop=True)
store = store.drop('Text25', axis=1)

store.rename(columns={'sBal': 'الرصيد عدد',
                      'sOutQty': 'الصادر عدد',
                      'sInQty': 'الوارد عدد',
                      'sLbl': 'اخر جرد عدد',
                      'نص98': 'اخر جرد وزن',
                      'نص97': 'الرصيد وزن',
                      'نص96': 'الصادر وزن',
                      'نص95': 'الوارد وزن',
                      "Text77": 'المخزن',
                      }, inplace=True)


fill_non_blank_down(store, 'ITM_NM')
fill_non_blank_down(store, 'itm_cd')

##############################
budget_detailed = pd.read_excel(r"D:\result\FILES\New folder (2)\SBOthAccRpt.xls")
budget_names = pd.read_excel(r"D:\result\FILES\New folder (2)\Sbaccmfrpt_BRF - Copy.xls")

give_name_for_NAN_in_another_col(budget_detailed, 'TR_DS', 'ماقبله', 'RACC', budget_names, 'acc_nm')
budget_detailed['tr_dt'] = budget_detailed['tr_dt'].replace(np.nan, "30/12/2022 00:00:00")
budget_detailed.rename(columns={'bal_D': 'الرصيد منه',
                      'bal_c': 'الرصيد له',
                      'mov_d': 'الحركة منه',
                      'mov_c': 'الحركة له',
                      }, inplace=True)
#make a new dataframe by drop rows in budget if minst3 is العملاءor الموردينor البنوك or الخزينة or اوراق قبض or اوراق دفع
budgetMainName=budget.drop (budget[(budget['minat3_name']=='العملاء')|(budget['minat3_name']=='الموردين')|(budget['minat3_name']=='البنوك')|(budget['minat3_name']=='الخزينه')|(budget['minat3_name']=='اوراق قبض')|(budget['minat3_name']=='اوراق دفع')].index)
#reset index
budgetMainName.reset_index(drop=True, inplace=True)
#drop 


bank_det = pd.read_excel(r"D:\result\FILES\New folder (2)\SBCshRpt.xls")
bank_names = pd.read_excel(r"D:\result\FILES\New folder (2)\Sbaccmfrpt_BRF.xls")
give_name_for_NAN_in_another_col(bank_det, 'mov_nm', 'ماقبله', 'Text66', bank_names, 'acc_nm')
bank_det['tr_dt']=bank_det['tr_dt'].replace(np.nan, "30/12/2022 00:00:00")
bank_det.rename(columns={'bal': 'الرصيد',
                        'inqty': 'مدين',
                        'outqty': 'دائن',
                        }, inplace=True)



##################################

with pd.ExcelWriter(r"D:\result\result.xlsx", engine="openpyxl") as writer:
    item_with_det.to_excel(writer, sheet_name='items_base')
    buying_df.to_excel(writer, sheet_name='buyvaluedf')
    selling_df.to_excel(writer, sheet_name='sellvalue')
    main_clint_df_t4.to_excel(writer, sheet_name='clint_database')
    budget.to_excel(writer, sheet_name='budget')
    lats_acc_stat.to_excel(writer, sheet_name='lats_acc_stat')
    sellhelper.to_excel(writer, sheet_name='sellhelper')
    store.to_excel(writer, sheet_name='store')
    goods_movements_df.to_excel(writer, sheet_name='goods_movem')
    budget_detailed.to_excel(writer, sheet_name='budget_detailed')
    bank_det.to_excel(writer, sheet_name='bank_det')
    budgetMainName.to_excel(writer, sheet_name='budgetMainName')


    end_time = timeit.default_timer()

print("Execution time:", end_time - start_time)
