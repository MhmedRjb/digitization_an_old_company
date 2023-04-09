def slice_barcode(df, new_column, thebarcode, frist_postion, last_postion, postion=0):

    df[new_column] = df[thebarcode].astype(str).str[frist_postion:last_postion]
    col = df.pop(new_column)
    df.insert(postion, col.name, col)
    return df
def fill_non_blank_down(df, column):
    """
    Fill NaN values in the specified column with the previous non-NaN value in the same column.
    """
    df[column] = df[column].fillna(method='bfill')
    df[column] = df[column].fillna(method='ffill')
    return df