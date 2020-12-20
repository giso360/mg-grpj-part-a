import pandas as pd

from preprocess_dfs import preprocess_books_df, generate_book_popularity_df, generate_author_popularity_df


pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)

df_author_popularity = generate_author_popularity_df()

print("=====  Book-Author | NOR (Top-100/Bottom-100) ======")

df_author_popularity_top_100 = df_author_popularity.head(100)
df_author_popularity_bottom_100 = df_author_popularity.tail(100)
print("==DESCRIBE==")
print(df_author_popularity.describe())
print("TOP-100")
print(df_author_popularity_top_100.describe())
print("BOTTOM-100")
print(df_author_popularity_bottom_100.describe())



print("===== OUTLIERS ======")
df_author_popularity_rating_mean = df_author_popularity["NOR"].mean()
df_author_popularity_rating_std = df_author_popularity["NOR"].std()
print(df_author_popularity_rating_mean, " / ", df_author_popularity_rating_std)

print("===Z-score conversion===")

df_author_popularity["Z-NOR"] = (df_author_popularity["NOR"] - df_author_popularity_rating_mean) / df_author_popularity_rating_std

print(df_author_popularity.head())
print(df_author_popularity.tail())


df_author_popularity_upper_outliers = df_author_popularity[df_author_popularity["Z-NOR"] > 3]
df_author_popularity_lower_outliers = df_author_popularity[df_author_popularity["Z-NOR"] < -3]

print("Top outliers")
print(df_author_popularity_upper_outliers.head(10))
print("Bottom outliers")
print(df_author_popularity_lower_outliers.head(10))