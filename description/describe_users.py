import pandas as pd
from part_a_util import report_if_field_is_unique, get_country


df_users = pd.read_csv('../data/BX-Users.csv', sep=';', encoding="ISO-8859-1")
# df_users = pd.read_csv('../data/user_tiny.csv', sep=';', encoding="ISO-8859-1")
print("=====COLUMNS/FIELDS=====")
print(df_users.columns, "\n")
df_fields = df_users.columns.tolist()
print("=====SHAPE=====")
print(df_users.shape, "\n")
print("=====DESCRIBE=====")
print(df_users.describe(), "\n")
print("=====INFO=====")
print(df_users.info, "\n")
age_mean = int(df_users["Age"].mean())
print("Mean value for Age field is: ", age_mean)
print("=====MEMORY USAGE=====")
print(df_users.info(memory_usage="deep"), "\n")
print("=====D-TYPES=====")
print(df_users.dtypes, "\n")
print("=====UNIQUES=====")
print("=====WHAT FIELDS ARE UNIQUE??====")

report_if_field_is_unique(df_users)
print("\n")
df_users_duplicates = df_users.drop_duplicates()
if df_users_duplicates.shape[0] == df_users.shape[0]:
    print("There are no duplicate records in datarfame")
else:
    print("There are duplicate records in datarfame: \n")
    print("Number of dupicate records: ", df_users_duplicates.shape[0] - df_users.shape[0])
print("=====NULL VALUES=====")
df_users[df_users["Age"].isnull()]
print("Nulls before: ", df_users[df_users["Age"].isnull()].shape[0])
print("Replace Nuls values .....")
for field in df_fields:
    if df_users[field].dtype != object:
        # Replace NaN with 0
        df_users[field] = df_users[field].fillna(0)
df_users[df_users["Age"].isnull()]
print("Nulls after: ", df_users[df_users["Age"].isnull()].shape[0])
print(df_users.describe())
print("\n")
print("=====ZERO VALUES=====")

df_users["Age"] = df_users["Age"].replace(0, age_mean)

print(df_users["Age"].mean())
print(df_users[df_users["Age"] == 0])
print(df_users.describe())
print("\n=====IRRATIONAL VALUES=====")
max_age = 122
df_users.loc[df_users["Age"] > max_age, "Age"] = age_mean
print("OK")
print(df_users.describe())
print("\n=====PRE-PROCESS LOCATION (KEEP COUNTRY)=====")
df_users["Location"] = df_users["Location"].apply(lambda x: get_country(x))  # To get country & keep relevant info & decrease memory
df_null_country = df_users[df_users["Location"] == "null_country"]
print("Number of user records with invalid locations in dataset: ", df_null_country.shape[0])

print("\n=========EXPORT TO CSV FOR DB MIGRATION===========\n")

df_users.to_csv("../migration/users_to_db.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")