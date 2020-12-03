import pandas as pd


pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)
df1 = pd.read_csv("./data/user_tiny.csv", sep=';', encoding="ISO-8859-1")
df2 = pd.read_csv("./data/ratiings_tiny.csv", sep=';', encoding="ISO-8859-1")
#
# indexNames = df[((df['Year-Of-Publication']) > 9999)].index
# df.drop(indexNames, inplace=True)
#
# # df = df.drop(len(df["Year-Of-Publication"] > 4), axis=1)
#
# print(df.head(10))

df = df2.merge(df1, on="User-ID", how="left")
print(df.head(10))
print("=========")
df = df2.merge(df1, on="User-ID", how="inner")
print(df.head(10))