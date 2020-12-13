import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import shutil
from PearsonsMetric import PearsonsMetric


def findKSimilar(r, k):
    # similarUsers is 2-D matrix
    similarities = np.ones((nUsers, nUsers))
    similarUsers = -1 * np.ones((nUsers, k))
    counter = 0
    for i in range(0, nUsers-1):
        for j in range(i, nUsers):
            sim = np.corrcoef(r[i], r[j])[0][1]
            similarities[i][j] = sim
            similarities[j][i] = sim
    for i in range(0, nUsers):
        simUsersIdxs = np.argsort(similarities[:, i])
        l = 0
        # find its most similar users
        for j in range(simUsersIdxs.size - 2, simUsersIdxs.size - k - 2, -1):
            simUsersIdxs[-k + 1:]
            similarUsers[i, l] = simUsersIdxs[j]
            l = l + 1
    return similarUsers, similarities




def findKSimilarPearson(r, k):
    # similarUsers is 2-D matrix
    similarities = np.ones((nUsers, nUsers))
    similarUsers = -1 * np.ones((nUsers, k))
    counter = 0
    for i in range(0, nUsers - 1):
        for j in range(i, nUsers):
            sim = PearsonsMetric(r[i], r[j]).get_pearson()
            similarities[i][j] = sim
            similarities[j][i] = sim
    for i in range(0, nUsers):
        simUsersIdxs = np.argsort(similarities[:, i])
        l = 0
        # find its most similar users
        for j in range(simUsersIdxs.size - 2, simUsersIdxs.size - k - 2, -1):
            simUsersIdxs[-k + 1:]
            similarUsers[i, l] = simUsersIdxs[j]
            l = l + 1
    return similarUsers, similarities



# Predict for 'userId', the rating of 'itemId'. 
# A trivial implementation of a collaboarative system
#
#'r': is the ratings matrix
#'userId': is the userId, and 
#'itemID': is the item id    
#'similarUsers': contains for each user his most similar users
#'similarities': are th pairwise cosine similarities between the users
# returns the prediction.     
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


# Range of interest for recommender is users that have rated between 31-40 times
# Who are these users???
ratings_lower_limit = 14
retings_upper_limit = 16
age_lower_limit = 19
age_upper_limit = 41
k = 5

sql_users_ages_in_recommender = """select distinct UserID from 
	                               (select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                                   group by UserID having no_of_ratings > %s and no_of_ratings < %s LIMIT 2000000) as rband
	                               where rband.UserID in 
	                               (SELECT UserID FROM books.users_table where Age > %s and Age < %s)"""

cursor.execute(sql_users_ages_in_recommender, (ratings_lower_limit, retings_upper_limit, age_lower_limit, age_upper_limit))
results = cursor.fetchall()
results_users = [el[0] for el in [e for e in results]]
print(results_users)
results_users.sort()



sql_ISBN_ages_in_recommender = """select distinct ISBN from books.ratings_table WHERE UserID in (select UserID from 
	                         (select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                              group by UserID having no_of_ratings > %s and no_of_ratings < %s LIMIT 2000000) as rband
	                         where rband.UserID in 
	                         (SELECT UserID FROM books.users_table where Age > %s and Age < %s))"""

cursor.execute(sql_ISBN_ages_in_recommender, (ratings_lower_limit, retings_upper_limit, age_lower_limit, age_upper_limit))
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




# Recommender
nUsers = len(results_users)
nItems = len(results_ISBN)
# r=np.array([[3,0,3,3],[5,4,0,2],[1,2,4,2],[2,2,0,1]])
r = df.to_numpy()
#r=np.random.rand(nUsers, nItems)

similarUsers, similarities=findKSimilar (r, k)





# similarUsers, similarities = findKSimilarPearson(r, k)

# Evaluation
start = datetime.now()
maei=0
mapei=0
counter = 0
for i in range(0,nUsers):
    for j in range(0, nItems):
        if r[i,j] != 0:
            rhat=predict (i,j,r, similarUsers, similarities)
            print (i, '-', j, 'prediction, real', rhat, r[i,j])
            if not np.isnan(rhat):
                counter += 1
                maei=maei+np.abs(rhat-r[i,j])
                mapei=mapei+np.abs((rhat-r[i,j])/r[i,j])
            
print('MAEI=', maei)
print('MAPEI=', mapei)
print("Counter: ", counter)
mae = maei/counter
print("MAE: ", mae)
mape = (mapei/counter)*100
print("MAPE= ", mape)



print("Calculation took approximately: ", (datetime.now() - start).seconds, " seconds")