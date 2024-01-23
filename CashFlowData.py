from UtilityFunctions import give_name_for_NAN_in_another_col
import pandas as pd
import numpy as np




def clean_the_data(clints_df, acc_stat):
    give_name_for_NAN_in_another_col(acc_stat, 'TR_DS', 'ماقبله', 'RACC', clints_df, 'acc_nm')
    acc_stat['tr_dt'] = acc_stat['tr_dt'].replace(np.nan, "30/12/2022 00:00:00")
    acc_stat['tr_dt'] = pd.to_datetime(acc_stat['tr_dt'], errors='coerce')
    acc_stat["days"] = acc_stat["tr_dt"].dt.day
    acc_stat = acc_stat.merge(clints_df, left_on='RACC',
                            right_on='acc_nm', how='left', suffixes=('_x', '_y'))
    return acc_stat



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





def preprocess_the_data(acc_stat,selling_df,clints_df):
    acc_stat['Libra'] = acc_stat.apply(lambda row: calculate_due_date(row['tr_dt'], row['max_time'],row['TR_DS']), axis=1)

    
    acc_stat["mov_d"] = acc_stat["mov_d"].fillna(0)
    acc_stat["mov_c"] = acc_stat["mov_c"].fillna(0)
    acc_stat["Total_bal"] = -(acc_stat["mov_d"]-acc_stat["mov_c"])*(1-acc_stat["tax"])
    cashFlow = acc_stat[['RACC', 'tr_dt', "mov_d", "mov_c", "TR_DS", 'Libra', 'max_time',
                            'days', 'tax', 'Total_bal', 'bal_D', "bal_c", "TEXT207", "TEXT208", "Text184"]].copy(deep=False)

    profit_df = pd.merge(clints_df[['acc_nm', 'tax']], selling_df,
                        left_on='acc_nm', right_on='acc_name', how='right', validate='one_to_many')
    profit_df = profit_df.drop(['acc_nm'], axis=1).reset_index(drop=True)

    profit_df['net_sell'] = np.where((profit_df['invoive_type'].str.contains(
        'بيع')), (profit_df['value']*(1-profit_df['tax'])), -(profit_df['value']*(1-profit_df['tax'])))

    profit_df['net_profit'] = np.where((profit_df['invoive_type'].str.contains('بيع')), ((
        profit_df['value']*(1-profit_df['tax'])) - profit_df['cost']),
        -((profit_df['value']*(1-profit_df['tax'])) - profit_df['cost']))
    profit_df['Profit Percentage(cost)'] = np.where((profit_df['invoive_type'].str.contains(
        'بيع')), (profit_df['net_profit'] / profit_df['cost']), -(profit_df['net_profit'] / profit_df['cost']))
    profit_df['Profit Percentage(value)'] = np.where((profit_df['invoive_type'].str.contains(
        'بيع')), (profit_df['net_profit'] / profit_df['value']), -(profit_df['net_profit'] / profit_df['value']))
    return cashFlow, profit_df


def cashFlowdata(clints_df, acc_stat, selling_df):
    # Load your dataframes, assuming acc_stat, selling_df, and clints_df are defined
    acc_stat = clean_the_data(clints_df,acc_stat) 
    profit_df,cashFlow = preprocess_the_data(acc_stat, selling_df, clints_df)  
    return profit_df, cashFlow




