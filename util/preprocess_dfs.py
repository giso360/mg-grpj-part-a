import pandas as pd
from util.part_a_util import get_country


def preprocess_users_df():
    df_users = pd.read_csv('../data/BX-Users.csv', sep=';', encoding="ISO-8859-1")
    # df_users = pd.read_csv('../data/user_tiny.csv', sep=';', encoding="ISO-8859-1")
    df_fields = df_users.columns.tolist()
    age_mean = int(df_users["Age"].mean())
    for field in df_fields:
        if df_users[field].dtype != object:
            # Replace NaN with 0
            df_users[field] = df_users[field].fillna(0)
    for field in df_fields:
        if df_users[field].dtype != object:
            # Replace 0 with mean
            df_users["Age"] = df_users["Age"].replace(0, age_mean)
    max_age = 122
    df_users.loc[df_users["Age"] > max_age, "Age"] = age_mean
    df_users["Location"] = df_users["Location"].apply(
        lambda x: get_country(x))  # To get country & keep relevant info & decrease memory
    return df_users


def preprocess_books_df():
    df_books = pd.read_csv('../data/BX-Books.csv', sep=';', encoding="ISO-8859-1")
    df_books = df_books.drop(columns=['Year-Of-Publication', 'Publisher', 'Image-URL-S', 'Image-URL-M', 'Image-URL-L'])
    df_books.dropna(axis=0, how='any', thresh=None, subset=None, inplace=True)
    return df_books


def preprocess_ratings_df():
    df_ratings = pd.read_csv('../data/BX-Book-Ratings.csv', sep=';', encoding="ISO-8859-1")
    # df_ratings = pd.read_csv('../data/ratiings_tiny.csv', sep=';', encoding="ISO-8859-1")
    df_ratings = df_ratings.drop_duplicates()
    df_ratings = df_ratings.drop_duplicates(["User-ID", "ISBN"], keep="last")
    return df_ratings


def generate_book_popularity_df():
    df_ratings = preprocess_ratings_df()
    a = df_ratings["ISBN"].value_counts()
    isbns = list(a.index)
    data = {"ISBN": isbns, "NOR": a}
    df_book_popularity = pd.DataFrame(data)
    df_book_popularity.reset_index(drop=True, inplace=True)
    return df_book_popularity


def generate_author_popularity_df():
    df_book_popularity = generate_book_popularity_df()
    df_books = preprocess_books_df()
    df_book_popularity_books = df_book_popularity.merge(df_books, on="ISBN", how="left")
    a = df_book_popularity_books["Book-Author"].value_counts()
    authors = list(a.index)
    data = {"Book-Author": authors, "NOR": a}
    df_author_popularity = pd.DataFrame(data)
    df_author_popularity.reset_index(drop=True, inplace=True)
    return df_author_popularity
