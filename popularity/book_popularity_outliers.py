import pandas as pd

from preprocess_dfs import preprocess_ratings_df, preprocess_books_df, generate_book_popularity_df

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)


df_book_popularity = generate_book_popularity_df()

print(df_book_popularity.head(100))
print(df_book_popularity.shape)
print(df_book_popularity.describe())
print(df_book_popularity.info())

print("===== ISBN | Title | NOR (Top-100) ======")
df_books = preprocess_books_df()
df_book_popularity_books = df_book_popularity.merge(df_books, on="ISBN", how="inner")

print(df_book_popularity_books.head())

df_book_popularity_books_top_100 = df_book_popularity_books.head(100)
print(df_book_popularity_books_top_100.describe())

df_book_popularity_books_bottom_100 = df_book_popularity_books.tail(100)
print(df_book_popularity_books_bottom_100.describe())


print("===== OUTLIERS ======")
df_book_popularity_rating_mean = df_book_popularity_books["NOR"].mean()
df_book_popularity_rating_std = df_book_popularity_books["NOR"].std()

df_book_popularity_rating_UCL = df_book_popularity_rating_mean + 3 * df_book_popularity_rating_std

df_book_popularity_rating_LCL = df_book_popularity_rating_mean - 3 * df_book_popularity_rating_std
print("UCL: ", df_book_popularity_rating_UCL)
print("LCL: ", df_book_popularity_rating_LCL)

print("===Z-score conversion===")

df_book_popularity_books["Z-NOR"] = (df_book_popularity_books["NOR"] - df_book_popularity_rating_mean) / df_book_popularity_rating_std

print(df_book_popularity_books.head())
print(df_book_popularity_books.tail())


df_book_popularity_books_upper_outliers = df_book_popularity_books[df_book_popularity_books["Z-NOR"] > 3]
df_book_popularity_books_lower_outliers = df_book_popularity_books[df_book_popularity_books["Z-NOR"] < -3]

print("Top outliers")
print(df_book_popularity_books_upper_outliers.tail(10))
print("Bottom outliers")
print(df_book_popularity_books_lower_outliers.head(10))