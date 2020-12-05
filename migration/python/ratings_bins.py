import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import pairwise_distances


def findKSimilar (r, k):
    
    # similarUsers is 2-D matrix
    similarUsers=-1*np.ones((nUsers,k))
    
    similarities=cosine_similarity(r)
       
    # for each user
    for i in range(0, nItems):
        simUsersIdxs= np.argsort(similarities[:,i])
        
        l=0
        #find its most similar users    
        for j in range(simUsersIdxs.size-2, simUsersIdxs.size-k-2,-1):
            simUsersIdxs[-k+1:]
            similarUsers[i,l]=simUsersIdxs[j]
            l=l+1
            
    return similarUsers, similarities


def predict(userId, itemId, r,similarUsers,similarities):

    # number of neighbours to consider
    nCols=similarUsers.shape[1]
    
    sum=0.0;
    simSum=0.0;
    for l in range(0,nCols):    
        neighbor=int(similarUsers[userId, l])
        #weighted sum
        sum= sum+ r[neighbor,itemId]*similarities[neighbor,userId]
        simSum = simSum + similarities[neighbor,userId]
    
    return  sum/simSum

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



plt.bar(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.values()), align='center')
plt.xticks(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.keys()))
plt.show()


# Range of interest for recommender is users that have rated between 31-40 times
# Who are these users???
sql_users_in_recommender = """select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                              group by UserID having no_of_ratings > 30 and no_of_ratings < 41 LIMIT 2000000"""

cursor.execute(sql_users_in_recommender)
results = cursor.fetchall()
results_users = [el[0] for el in [e for e in results]]
print(results_users)
results_users.sort()



sql_ISBN_in_recommender = """SELECT distinct ISBN from books.ratings_table where UserID in
                             (select distinct UserID from books.ratings_table group by UserID
                             having COUNT(*) > 30 and COUNT(*) < 41) LIMIT 2000000"""
cursor.execute(sql_ISBN_in_recommender)
results = cursor.fetchall()
results_ISBN = [el[0] for el in [e for e in results]]
print(results_ISBN)
results_ISBN.sort()

# Close db connection
db.close()

df_for_recommender = pd.read_csv("../ratings_to_db.csv", sep=";", encoding="ISO-8859-1")
df_for_recommender = df_for_recommender[df_for_recommender["User-ID"].isin(results_users)]
print(df_for_recommender.shape)
print("the recommender focuses on number of ratings for the prescribed bin: ", df_for_recommender.shape[0])
print("Ratings for number of users: ", df_for_recommender["User-ID"].nunique())

mean_ratings = df_for_recommender['Book-Rating'].mean()

df = pd.DataFrame(index = results_users, columns = results_ISBN)

for index, row in df_for_recommender.iterrows():
    df.loc[row['User-ID'], row['ISBN']] = row['Book-Rating']
    
df = df.fillna(value = 0)  
    
def predict2(ratings, similarity):
    mean_user_rating = mean_ratings
    ratings_diff = (ratings - mean_user_rating)
    pred = mean_user_rating + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis = 1)])
    
user_similarity = pairwise_distances(df, metric='cosine')
user_prediction = predict2(df, user_similarity)


# df_zero = pd.DataFrame(index = [-a for a in range (0, 26398)], columns = results_ISBN)
# df_zero.fillna(value = 0)
    
# df = df.fillna(value = 0)    
# df = df[(df.T != 0).any()]

# # RECOMMENDER #

# nUsers = len(results_users)
# nItems = len(results_ISBN)
# recommender = df.to_numpy()

# similarUsers, similarities = findKSimilar (recommender, 7)

# mae=0
# for i in range(0,nUsers):
#     for j in range(0, nItems):
#         rhat=predict (i,j,recommender, similarUsers, similarities)
#         print ('prediction, real',rhat,recommender[i,j])
#         mae=mae+np.abs(rhat-recommender[i,j])
# print ('MAE=',mae)

