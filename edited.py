import numpy as np
import pandas as pd

path_to_item_file = r"D:\New folder (2)\item_data.xlsx"
path_to_item_file2 = r'D:\New folder (2)\item_df.xlsx'
item_df = pd.read_excel(path_to_item_file)
item_df2 = pd.read_excel(path_to_item_file2)

item_df.columns = ['Text139', 'barcode', 'item', 'quntity', 'typo', 'SLS_UNT', 'PRC1', 'PRC2']

item_df = item_df.dropna(subset=['item', 'quntity']).reset_index(drop=True)


def add_left_zero(df, codel_col):
    df[codel_col] = '0' + df[codel_col].astype('int32').astype('str')


add_left_zero(item_df2, 'code')
add_left_zero(item_df, 'barcode')


def slice_barcode(df, new_column,thebarcode ,x, y, postion=0):
    df[new_column] = df[thebarcode].astype(str).str[x:y]
    col = df.pop(new_column)
    df.insert(postion, col.name, col)


slice_barcode(item_df, 'barcode_T1', 'barcode',0, 2, 0)
slice_barcode(item_df, 'barcode_T2', 'barcode',0, 4, 1)


def codetoname(target_df, translatr_df, DIC_KEY, DIC_value, traget_code_col, new_name_col):
    translator = {}
    for i in range(0, translatr_df.shape[0]):
        translator[translatr_df[DIC_KEY][i]] = translatr_df[DIC_value][i]
    target_df[new_name_col] = target_df[traget_code_col].map(translator)


codetoname(item_df, item_df2, 'code', 'item', 'barcode_T1', 'barcode_T1_name')
codetoname(item_df, item_df2, 'code', 'item', 'barcode_T2', 'barcode_T2_name')
codetoname(item_df, item_df2, 'code', 'item', 'barcode', 'barcode_name')

item_df['Libra officer'] = np.where((item_df['barcode_T2'].astype(str).str.contains(r'\b010[1,3].*')),
                                    12.5, 
                            np.where( item_df['barcode'].astype(str).str.contains(r'\b0201.*[4-5].*|\b0202.*[3].*'),
                                    9,
                            np.where(item_df['barcode'].astype(str).str.contains(r'\b030[3-7]0[1].*|\b030602.*'), 
                                    10,
                            np.where(item_df['barcode'].astype(str).str.contains(r'\b04010[1-3]|030203'), 
                                    18,
                            np.where((item_df['barcode'].astype(str).str.contains(r'0102002')), 
                            32.5 ,
                                              np.where((item_df['barcode'].astype(str).str.contains(r'010200[3-4]')), 52
                                                       , np.where(
                                                      (item_df['barcode'].astype(str).str.contains(r'0102005')), 104
                                                          , np.where(
                                                              (item_df['barcode'].astype(str).str.contains(r'0102001')),
                                                              12.5
                                                              , 1))))))))


##########################
test = pd.read_excel(r"D:\result\FILES\ALL_ABOUT.xlsx")
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
clints_df = pd.read_excel(r"C:\Users\mohamed\Desktop\newnew.xlsx")
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

acc_stat = pd.read_excel(r"C:\Users\mohamed\Desktop\CCCCCCCCCC.xlsx")
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
acc_stat["Total_bal"]=(acc_stat["mov_d"]-acc_stat["mov_c"])*(1-acc_stat["tax"])

lats_acc_stat = acc_stat[['RACC','tr_dt',"mov_d","mov_c","TR_DS",'Libra','max_time','days','tax','Total_bal','bal_D',"bal_c"]].copy(deep=False)

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





#############################
import numpy as np
import pandas as pd

budget = pd.read_excel(r"D:\New folder (2)\helo.xlsx")
budget['Acc_cd'] = budget['Acc_cd'].replace(r'[^0-9]', np.nan, regex=True)
budget = budget.dropna(subset=['Acc_cd']).reset_index(drop=True)
budget['Acc_cd'] = budget['Acc_cd'].astype('int32').astype('str')
print(budget.head(22))


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
    for i in range(1, 261):
        if pd.isna(df.loc[i, column]) is False:
            h = df.loc[i, column]
        else:
            df.loc[i, column] = h

for i in range(1,9):
    codetoname(budget,budget,'Acc_cd','Acc_nm','minat'+str(i),'minat'+str(i)+'_name')


# codetoname(budget,budget,'Acc_cd','Acc_nm','minat1','minat1_name')
# codetoname(budget,budget,'Acc_cd','Acc_nm','minat2','minat2_name')
# codetoname(budget,budget,'Acc_cd','Acc_nm','minat3','minat3_name')
# codetoname(budget,budget,'Acc_cd','Acc_nm','minat5','minat5_name')
# codetoname(budget,budget,'Acc_cd','Acc_nm','minat6','minat6_name')
# codetoname(budget,budget,'Acc_cd','Acc_nm','minat8','minat8_name')


all_nonblanck_down(budget, 'minat1_name')
all_nonblanck_down(budget, 'minat2_name')
all_nonblanck_down(budget, 'minat3_name')
all_nonblanck_down(budget, 'minat5_name')
all_nonblanck_down(budget, 'minat6_name')
all_nonblanck_down(budget, 'minat8_name')

budget.drop(budget.columns[[0,1,2,3,4,5,6,7,8,9,10,11,12,13]], axis=1, inplace=True)
budget.columns = budget.columns.str.replace('DbBal', 'الحركة مدين')
budget.columns = budget.columns.str.replace('CrBal', 'الحركة دائن')
budget.columns = budget.columns.str.replace('Label113', 'مدين نهاية المدة ')
budget.columns = budget.columns.str.replace('Text153', 'مدين أول المدة ')
budget.columns = budget.columns.str.replace('Text154', 'دائن اول  المدة ')
budget.columns = budget.columns.str.replace('Text161', 'دائن اخر المدة')









##############################

with pd.ExcelWriter(r"D:\result\result.xlsx") as writer:
    item_df.to_excel(writer, sheet_name='items_base')
    buyvaluedf.to_excel(writer, sheet_name='buyvaluedf')
    sellvalue.to_excel(writer, sheet_name='sellvalue')
    main_clint_df_t4.to_excel(writer, sheet_name='clint_database')
    budget.to_excel(writer, sheet_name='budget')
    lats_acc_stat.to_excel(writer, sheet_name='lats_acc_stat')



