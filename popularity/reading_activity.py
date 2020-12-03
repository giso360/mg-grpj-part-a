from util.part_a_util import sort_dict_by_value_desc
from util.preprocess_dfs import *
from datetime import datetime

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', None)
start = datetime.now()

df_books = preprocess_books_df()
df_users = preprocess_users_df()
df_ratings = preprocess_ratings_df()

df_users_ratings = df_ratings.merge(df_users, on="User-ID", how="left")
print("-------")
print(df_users_ratings.head(10))
print("-------")
print("ages:")
df_users_ratings_books = df_users_ratings.merge(df_books, on="ISBN", how="left")
print(sorted(df_users_ratings_books["Age"].unique().tolist()))
age_mean = int(df_users_ratings_books["Age"].mean())
print(age_mean)

# df_users_ratings_books['Age'] = df_users_ratings_books['Age'].fillna(age_mean)

print(sorted(df_users_ratings_books["Age"].unique().tolist()))

grouped_users_ratings_books = df_users_ratings_books.groupby(["User-ID"])

users = df_users_ratings_books["User-ID"].unique().tolist()

user_no_ratings = {}
for user in users:
    user_no_ratings[user] = grouped_users_ratings_books.get_group(int(user))["Book-Rating"].count()

user_no_ratings = sort_dict_by_value_desc(user_no_ratings)
mean_ratings_per_user = sum(user_no_ratings.values()) / len(user_no_ratings)
rating_matrix_df = pd.DataFrame(user_no_ratings.items(), columns=["User-ID", "No-Of-Ratings"])
print(rating_matrix_df.head(10))

print("Calculation took approximately: ", (datetime.now() - start).seconds, " seconds")

df_ratings_matrix_w_ages = rating_matrix_df.merge(df_users, on="User-ID", how="inner")

# df_ratings_matrix_w_ages['Age'] = df_ratings_matrix_w_ages['Age'].fillna(age_mean)

df_ratings_matrix_w_ages = df_ratings_matrix_w_ages.drop(columns=["Location"])

df_ratings_matrix_w_ages.to_csv("../data/rating_matrix.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")

# # SOS - FOR POPULARITY
# # print(df_ratings.value_counts())
# # print(type(df_ratings.value_counts()))
# # # SOS