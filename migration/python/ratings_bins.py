import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root")

cursor = db.cursor()

cursor.execute("use books")

bins_and_number_of_ratings = {}
for i in range(0, 150, 10):
    y = i + 10
    print(i, y)
    sql = """select Count(*) from (select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table group by UserID 
             having (no_of_ratings > %s  AND no_of_ratings <= %s) LIMIT 2000000) AS ag"""
    cursor.execute(sql, (i, y))
    result = list(cursor.fetchall())
    bins_and_number_of_ratings[y] = result[0][0]
    


# Close db connection

plt.bar(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.values()), align='center')
plt.xticks(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.keys()))
plt.show()


# Range of interest for recommender is users that have rated between 31-40 times
# Who are these users???
sql_users_in_recommender = """select distinct UserID, COUNT(*) as no_of_ratings
from books.ratings_table
group by UserID
having no_of_ratings > 30
and no_of_ratings < 41
LIMIT 2000000;"""

cursor.execute(sql_users_in_recommender)
results = cursor.fetchall()
results_users = [el[0] for el in [e for e in results]]
print(results_users)
db.close()

df_for_recommender = pd.read_csv("../ratings_to_db.csv", sep=";", encoding="ISO-8859-1")
df_for_recommender = df_for_recommender[df_for_recommender["User-ID"].isin(results_users)]
print(df_for_recommender.shape)
print("the recommender focuses on number of ratings for the prescribed bin: ", df_for_recommender.shape[0])
print("Ratings for number of users: ", df_for_recommender["User-ID"].nunique())

# RECOMMENDER #






