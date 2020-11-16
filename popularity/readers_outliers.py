import pandas as pd

df_readers_ratings = pd.read_csv('../data/rating_matrix.csv', sep=';', encoding="ISO-8859-1")

print(df_readers_ratings.describe())

NOR_mean = df_readers_ratings["No-Of-Ratings"].mean()
NOR_std = df_readers_ratings["No-Of-Ratings"].std()


df_readers_ratings["Z-NOR"] = (df_readers_ratings["No-Of-Ratings"] - NOR_mean) / NOR_std

df_readers_ratings_upper_outliers = df_readers_ratings[df_readers_ratings["Z-NOR"] > 3]
df_readers_ratings_lower_outliers = df_readers_ratings[df_readers_ratings["Z-NOR"] < -3]

print("READER OUTLIERS")
# print(df_readers_ratings_upper_outliers.head())
print(df_readers_ratings_upper_outliers.tail())
print("----------------------------------------")
# print(df_readers_ratings_lower_outliers.head())
print(df_readers_ratings_lower_outliers.tail())

print("RRRRRRRRR")

print(df_readers_ratings["Z-NOR"].mean())




