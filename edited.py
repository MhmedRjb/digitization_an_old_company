import numpy as np
import pandas as pd

def add_left_zero(df, codel_col):
    df[codel_col] = '0' + df[codel_col].astype('int32').astype('str')

def slice_barcode(df, new_column,thebarcode ,x, y, postion=0):
    df[new_column] = df[thebarcode].astype(str).str[x:y]
    col = df.pop(new_column)
    df.insert(postion, col.name, col)

def codetoname(target_df, translatr_df, DIC_KEY, DIC_value, traget_code_col, new_name_col):
    translator = {}
    for i in range(0, translatr_df.shape[0]):
        translator[translatr_df[DIC_KEY][i]] = translatr_df[DIC_value][i]
    target_df[new_name_col] = target_df[traget_code_col].map(translator)


##########################
test = pd.read_excel(r"D:\result\FILES\New folder (2)\SBJRNLITMRPTTAX.xlsx")
"clean the data"
test = test.dropna(axis='columns', how="all")
test.columns = ['Inv_No', 'Inv', 'acc_name', 'cost',
                'value', 'tax', 'discount', 'unitprice',
                'quantity', 'type', 'invoive_type',
                'item_NAME', 'ITEM_CODE', 'INVOICE_T1', 'INVOICE', 'DATE']
"filter the data"
buyvaluedf = test[(test['invoive_type'].str.contains('مرتد|شراء'))].reset_index(drop=True)

buyvaluedf['buying_total'] = np.where(buyvaluedf['invoive_type'].str.contains('شراء'),buyvaluedf['cost']
                                ,-buyvaluedf['value'])

buyvaluedf['quantity_total'] = np.where(buyvaluedf['invoive_type'].str.contains('شراء'), buyvaluedf['quantity']
                                ,-buyvaluedf['quantity'])

sellvalue = test[(test['invoive_type'].str.contains('مرتجع|بيع'))].reset_index(drop=True)

"get what you need from the data"
sellvalue['gross_profit'] = np.where((sellvalue['invoive_type'].str.contains('بيع')), sellvalue['value'] - sellvalue['cost']
                               , -(sellvalue['value'] - sellvalue['cost']))

sellvalue['gross_sell']= np.where((sellvalue['invoive_type'].str.contains('بيع')),sellvalue['value']
                                ,-(sellvalue['value']))

sellvalue['total_quantity'] = np.where((sellvalue['invoive_type'].str.contains('بيع')), sellvalue['quantity']
                                , -(sellvalue['quantity']))

sellvalue = sellvalue.drop(['tax'],axis=1).reset_index(drop=True)



############################
clints_df = pd.read_excel(r"D:\result\FILES\New folder (2)\SBAccMFDtlRpt (3).xlsx")
clints_df = clints_df.replace(r'^\s*$', np.nan, regex=True)
clints_df.drop(clints_df.index[clints_df['acc_nm'].isnull() ], inplace = True)

clints_df['acc_cd'] =  clints_df['acc_cd'].astype('int32').astype('str')
clints_df=clints_df.reset_index()

main_clint_df_t4=clints_df[(clints_df['acc_nm'].str.contains('^(?!فروع).*$'))&(clints_df['acc_cd'].str.contains('.2.....{0,2}$'))].reset_index(drop=True)


slice_barcode(main_clint_df_t4,'minat1','acc_cd',0,3,0)
slice_barcode(main_clint_df_t4,'minat2','acc_cd',0,4,1)
slice_barcode(main_clint_df_t4,'minat3','acc_cd',0,6,2)
codetoname(main_clint_df_t4,clints_df,'acc_cd','acc_nm','minat1','minat1_name')
codetoname(main_clint_df_t4,clints_df,'acc_cd','acc_nm','minat2','minat2_name')
codetoname(main_clint_df_t4,clints_df,'acc_cd','acc_nm','minat3','minat3_name')

main_clint_df_t4['tax'] = np.where(main_clint_df_t4['minat3'].astype(str).str.contains('123101.*'), 0.08,
                            np.where(main_clint_df_t4['minat3'].astype(str).str.contains('123104.*'), 0.04,
                                     np.where(main_clint_df_t4['minat3'].astype(str).str.contains('12310[2,3].*'), 0.01,
                                              0.00)))

#############################

clints_df.columns = ['index', 'empty1', 'empty2', 'code','acc_nm','mony_forus','mony_onus','place','empty3','empty4','empty5',
                     'empty5',"man","max_mony","max_time"]

clints_df["max_time"]=clints_df["max_time"].astype("int32")

acc_stat = pd.read_excel(r"D:\result\FILES\New folder (2)\SBACCRPTA4 (2).xlsx")
acc_stat.drop(['Text139', 'نص204'], axis=1)
clints_df['acc_nm'] = clints_df['acc_nm'].fillna(0)


def give_name_for_NAN_in_another_col(traget_df,badeling_col,badeling_value,changabel_col,insert_df,insert_value):
    j=-1
    for i in range(0, traget_df.shape[0]):
        if traget_df.loc[i, badeling_col] == badeling_value:
            j = j + 1
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]
        else:
            traget_df.loc[i, changabel_col] = insert_df.loc[j, insert_value]

give_name_for_NAN_in_another_col(acc_stat,'TR_DS','ماقبله','RACC',clints_df,'acc_nm')
'replace np.nat with 0'
acc_stat['tr_dt'] = acc_stat['tr_dt'].replace(np.nan, "30/12/2022 00:00:00")

acc_stat['tr_dt'] = pd.to_datetime(acc_stat['tr_dt'], errors='coerce')

acc_stat["days"]=acc_stat["tr_dt"].dt.day

acc_stat = acc_stat.merge(clints_df, left_on='RACC', right_on='acc_nm', how='left',suffixes=('_x', '_y'))

acc_stat = acc_stat.merge(main_clint_df_t4, left_on='RACC', right_on='acc_nm', how='left',suffixes=('_x', '_y'))

acc_stat['Libra'] = np.where((acc_stat['TR_DS'].astype(str).str.contains(r"مدين|دائن"))
                                    ,acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(0, unit='d'), 
                    np.where((acc_stat['max_time']==15)
                                    ,acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(15, unit='d'), 
                    np.where((acc_stat['max_time']==21)
                                    ,acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(21, unit='d'),
                    np.where( (acc_stat['max_time']==222), 
                                    acc_stat["tr_dt"].dt.to_period('M').dt.end_time + pd.Timedelta(14, unit='d'),
                    np.where((acc_stat['max_time']==45), 
                                    acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(45, unit='d'),
                    np.where((acc_stat['max_time']==3), 
                                    acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(3, unit='d'),
                    np.where((np.logical_and((acc_stat['max_time']==333),(acc_stat['days']<15))), 
                                    acc_stat["tr_dt"].dt.to_period('M').dt.start_time + pd.Timedelta(21, unit='d'),
                    np.where((np.logical_and((acc_stat['max_time']==333),(acc_stat['days']>=15))),
                                    acc_stat["tr_dt"].dt.to_period('M').dt.end_time + pd.Timedelta(7, unit='d'),
                    acc_stat["tr_dt"].dt.to_period('d').dt.start_time + pd.Timedelta(0, unit='d')
                     ))))))))



acc_stat["mov_d"]=acc_stat["mov_d"].fillna(0)
acc_stat["mov_c"]=acc_stat["mov_c"].fillna(0)
acc_stat["Total_bal"]=-(acc_stat["mov_d"]-acc_stat["mov_c"])*(1-acc_stat["tax"])

lats_acc_stat = acc_stat[['RACC','tr_dt',"mov_d","mov_c","TR_DS",'Libra','max_time','days','tax','Total_bal','bal_D',"bal_c","TEXT207"]].copy(deep=False)



sellvalue = pd.merge(main_clint_df_t4[['acc_nm', 'tax']],sellvalue , left_on='acc_nm',right_on='acc_name',how='right',validate='one_to_many')
sellvalue = sellvalue.drop(['acc_nm'],axis=1).reset_index(drop=True)

sellvalue['net_sell']= np.where((sellvalue['invoive_type'].str.contains('بيع')),(sellvalue['value']*(1-sellvalue['tax']))
                        ,-(sellvalue['value']*(1-sellvalue['tax'])))

sellvalue['net_profit'] = np.where((sellvalue['invoive_type'].str.contains('بيع')), ((sellvalue['value']*(1-sellvalue['tax'] ))- sellvalue['cost'])
                               , -((sellvalue['value']*(1-sellvalue['tax'] ))- sellvalue['cost']))
sellvalue['Profit Percentage(cost)'] = np.where((sellvalue['invoive_type'].str.contains('بيع')), (sellvalue['net_profit'] /sellvalue['cost'])
                               , -(sellvalue['net_profit'] /sellvalue['cost']))
sellvalue['Profit Percentage(value)'] = np.where((sellvalue['invoive_type'].str.contains('بيع')), (sellvalue['net_profit'] /sellvalue['value'])
                               , -(sellvalue['net_profit'] /sellvalue['value']))


helprt_acc=[lats_acc_stat['TR_DS'] .str.contains('مرتجع|بيع')]
helprt_acc=lats_acc_stat.groupby(['RACC','Libra','tr_dt'])['Total_bal'].sum().reset_index()

sellhelper=sellvalue['DATE'].agg(['min', 'max'])
sellhelper["# of days"] = (sellhelper["max"] - sellhelper["min"])/ np.timedelta64(1, 'D')
sellhelper["# of weeks"] = (sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'W')
sellhelper["# of months"] = (sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'M')
sellhelper["#3 of months"] = (sellhelper["max"] - sellhelper["min"]) / np.timedelta64(3, 'M')
# sellhelper["# of years"] = (sellhelper["max"] - sellhelper["min"]) / np.timedelta64(1, 'Y')
#############################



##############################

def add_left_zero(df, codel_col):
    df[codel_col] = '0' + df[codel_col].astype('int32').astype('str')

def slice_barcode(df, new_column,thebarcode ,x, y, postion=0):
    df[new_column] = df[thebarcode].astype(str).str[x:y]
    col = df.pop(new_column)
    df.insert(postion, col.name, col)

def codetoname(target_df, translatr_df, DIC_KEY, DIC_value, traget_code_col, new_name_col):
    translator = {}
    for i in range(0, translatr_df.shape[0]):
        translator[translatr_df[DIC_KEY][i]] = translatr_df[DIC_value][i]
    target_df[new_name_col] = target_df[traget_code_col].map(translator)

all_item = pd.read_excel(r"D:\result\FILES\New folder (2)\Sbitmsmfrpt_ORG.xlsx")
item_with_det = pd.read_excel(r"C:\Users\mohamed\Desktop\item_with_det.xlsx")
all_item = all_item.dropna(subset=['itm_cd']).reset_index(drop=True)
item_with_det = item_with_det.dropna(subset=['itm_cd']).reset_index(drop=True)

add_left_zero(all_item,'itm_cd')
add_left_zero(item_with_det,'itm_cd')

slice_barcode(item_with_det, 'itm_cd_T1', 'itm_cd',0, 2, 0)
slice_barcode(item_with_det, 'itm_cd_T2', 'itm_cd',0, 4, 1)

codetoname(item_with_det, all_item,'itm_cd','ITM_NM','itm_cd_T1','itm_cd_T1_name')
codetoname(item_with_det, all_item,'itm_cd','ITM_NM','itm_cd_T2','itm_cd_T2_name')

##########################

sellvalue = sellvalue.drop(['tax'],axis=1).reset_index(drop=True)

############################

budget = pd.read_excel(r"D:\result\FILES\New folder (2)\SBaccTriRpt.xlsx")
budget['Acc_cd'] = budget['Acc_cd'].replace(r'[^0-9]', np.nan, regex=True)
budget = budget.dropna(subset=['Acc_cd']).reset_index(drop=True)
budget['Acc_cd'] = budget['Acc_cd'].astype('int32').astype('str')

slice_barcode(budget,'minat1','Acc_cd',0,1,0)
slice_barcode(budget,'minat2','Acc_cd',0,2,1)
slice_barcode(budget,'minat3','Acc_cd',0,3,2)
slice_barcode(budget,'minat4','Acc_cd',0,4,3)
slice_barcode(budget,'minat5','Acc_cd',0,5,4)
slice_barcode(budget,'minat6','Acc_cd',0,6,5)
slice_barcode(budget,'minat7','Acc_cd',0,7,6)
slice_barcode(budget,'minat8','Acc_cd',0,8,7)
slice_barcode(budget,'minat9','Acc_cd',0,9,7)

def all_nonblanck_down(df, column):
    h = 0
    for i in range(1, df.shape[0]):
        if pd.isna(df.loc[i, column]) is False:
            h = df.loc[i, column]
        else:
            df.loc[i, column] = h
    return df
codetoname(budget,budget,'Acc_cd','Acc_nm','minat1','minat1_name')
codetoname(budget,budget,'Acc_cd','Acc_nm','minat2','minat2_name')
codetoname(budget,budget,'Acc_cd','Acc_nm','minat3','minat3_name')
codetoname(budget,budget,'Acc_cd','Acc_nm','minat5','minat5_name')
codetoname(budget,budget,'Acc_cd','Acc_nm','minat6','minat6_name')
codetoname(budget,budget,'Acc_cd','Acc_nm','minat8','minat8_name')
print(budget.shape[0])

all_nonblanck_down(budget, 'minat1_name')
all_nonblanck_down(budget, 'minat2_name')
all_nonblanck_down(budget, 'minat3_name')
all_nonblanck_down(budget, 'minat5_name')
all_nonblanck_down(budget, 'minat6_name')
all_nonblanck_down(budget, 'minat8_name')

budget.drop(budget.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
budget.rename(columns = {'DbBal':'الحركة مدين', 
                         'CrBal':'الحركة دائن', 
                         'Label113':'مدين نهاية المدة ', 
                         'Text153':'مدين أول المدة ',
                         'Text154':'دائن اول  المدة ',
                         'Text161': 'دائن اخر المدة'}, inplace = True)



##############################
  
store = pd.read_excel(r"D:\result\FILES\New folder (2)\SBINQALLRPT_CTRL (2).xlsx")
store['itm_cd'] = store['itm_cd'].replace(r'[^0-9]', np.nan, regex=True).reset_index(drop=True)
print(store.shape[0])
all_nonblanck_down(store, 'ITM_NM')
all_nonblanck_down(store, 'itm_cd')


##############################

with pd.ExcelWriter(r"D:\result\result.xlsx",engine="openpyxl") as writer:
    item_with_det.to_excel(writer, sheet_name='items_base')
    buyvaluedf.to_excel(writer, sheet_name='buyvaluedf')
    sellvalue.to_excel(writer, sheet_name='sellvalue')
    main_clint_df_t4.to_excel(writer, sheet_name='clint_database')
    budget.to_excel(writer, sheet_name='budget')
    lats_acc_stat.to_excel(writer, sheet_name='lats_acc_stat')
    sellhelper.to_excel(writer, sheet_name='sellhelper')
    store.to_excel(writer, sheet_name='store')






