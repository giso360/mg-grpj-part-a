import pandas as pd
from util.part_a_util import report_if_field_is_unique



df_ratings = pd.read_csv('../data/BX-Book-Ratings.csv', sep=';', encoding="ISO-8859-1")
print("=====COLUMNS/FIELDS=====")
print(df_ratings.columns, "\n")
df_fields = df_ratings.columns.tolist()
print("=====SHAPE=====")
print(df_ratings.shape, "\n")
print("=====DESCRIBE=====")
print(df_ratings.describe(), "\n")
print("=====INFO=====")
print(df_ratings.info, "\n")
print("=====MEMORY USAGE=====")
print(df_ratings.info(memory_usage="deep"), "\n")
print("=====D-TYPES=====")
print(df_ratings.dtypes, "\n")
print("=====UNIQUES=====")
# print(len(df_users["User-ID"].unique()) == df_users.shape[0])
# print(len(df_users["Location"].unique()) == df_users.shape[0])
# print(len(df_users["Age"].unique()) == df_users.shape[0])
print("=====WHAT FIELDS ARE UNIQUE??====")
df_ratings['ISBN'] = df_ratings['ISBN'].apply(lambda x:x.lower())
report_if_field_is_unique(df_ratings)
print("\n")
print("=========")
df_ratings = df_ratings.drop_duplicates()
initial_size = df_ratings.shape[0]
df_ratings = df_ratings.drop_duplicates(["User-ID", "ISBN"], keep="last")
final_size = df_ratings.shape[0]
if initial_size != final_size:
    print(initial_size - final_size, "Duplicates with common ISBN, User-ID Pairs detected AND removed")
else:
    print("No Duplicates with common ISBN, User-ID Pairs detected")



print(len(df_ratings["User-ID"].unique().tolist()))

print("CSV to DB")

df_ratings.to_csv("../migration/ratings_to_db.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")
