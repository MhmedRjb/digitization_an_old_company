def add_left_zero(df, codel_col):
    df[codel_col] = '0' + df[codel_col].astype('int32').astype('str')
