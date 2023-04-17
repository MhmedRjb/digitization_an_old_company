import pandas as pd

clints_file_an_ordianty = pd.read_excel(r"D:\SBJRNLITMRPTTAXCLINTS.xls")
non_clints_file_an_ordianty = pd.read_excel(r"D:\SBJRNLITMRPTTAXWITHOUTCLNYD.xls")
print(clints_file_an_ordianty.shape)
print(non_clints_file_an_ordianty.shape)
for col in clints_file_an_ordianty.columns:
    print([clints_file_an_ordianty].col)
if set(clints_file_an_ordianty.columns) != set(non_clints_file_an_ordianty.columns):
    print("The column names in the two dataframes are different.")
else:
    print("The two dataframes have the same number and names of columns.")
