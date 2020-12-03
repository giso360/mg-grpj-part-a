import sys
import pandas as pd
import matplotlib.pyplot as plt
# from util.part_a_util import report_if_field_is_unique
# sys.path.append('../util')


def report_if_field_is_unique(df):
    fields = df.columns.tolist()
    for field in fields:
        if len(df[field].unique()) == df.shape[0]:
            print("Field [", str(field), "] is unique")
        else:
            print("Field [", str(field), "] is NOT unique")

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
df_ratings['ISBN'] = df_ratings['ISBN'].apply(lambda x: x.lower())
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
# exclude rows for users with a single rating

# indexNames = df[((df['Year-Of-Publication']) > 9999)].index
# df.drop(indexNames, inplace=True)
print(df_ratings.shape)
print("====AND====")
print(df_ratings["User-ID"].nunique()) # 105283 users have provided book ratings out of the total of 278858 registered users
df_ratings_freq_analysis = df_ratings.groupby(["User-ID"])["User-ID"].count().reset_index(name="count")
print(df_ratings_freq_analysis.columns)
print(df_ratings_freq_analysis.dtypes)
print("bla")
# TODO: Create bins/histogram for reading activity (cut function)
df_ratings_freq_analysis.astype({"count": "int32"})
bins = pd.cut(df_ratings_freq_analysis["count"], [*range(0, 14000, 150)])
df_ratings_freq_analysis_bins = df_ratings_freq_analysis.groupby(bins)["count"].agg(["count"])
print(df_ratings_freq_analysis_bins.head(100))
print(df_ratings_freq_analysis_bins.columns)
print("--------------------")
df_ratings_freq_analysis_bins_intresting = df_ratings_freq_analysis[df_ratings_freq_analysis.groupby(["User-ID"]) <= 150]
print(df_ratings_freq_analysis_bins_intresting.head())
print("pppp")
bins = pd.cut(df_ratings_freq_analysis_bins_intresting["count"], [*range(0, 150, 10)])
df_ratings_freq_analysis_bins_intresting_bins = df_ratings_freq_analysis_bins_intresting.groupby(bins)["count"]
print(df_ratings_freq_analysis_bins_intresting_bins.head(100))
# Need Histogram
# df_ratings_freq_analysis_bins.hist(bins=150)
# df_ratings_freq_analysis_bins.plot.hist()
# plt.show()

# #######################
print(df_ratings_freq_analysis_bins["count"].sum())
print("bla")


print(df_ratings_freq_analysis.describe())

print("====AND====")
print(df_ratings.head())
df_ratings_count_single_indexes = df_ratings[df_ratings['User-ID'].map(df_ratings['User-ID'].value_counts()) == 1].index
df_ratings.drop(df_ratings_count_single_indexes, inplace=True)
df_ratings.reset_index(drop=True, inplace=True)
print(df_ratings.shape)
df_ratings.to_csv("../migration/ratings_to_db.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")
