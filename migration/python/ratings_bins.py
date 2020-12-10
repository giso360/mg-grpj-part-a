import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import shutil

# Find the k-most similar users for each user
#
# r is the ratings matrix
# k is the number of most similar users
#
# returns: '
#similarUsers: contains the indices of the most similar users to each user
# similarities: is the pairwise similarities, i.e. similarities between users
def findKSimilar (r, k):
    
    # similarUsers is 2-D matrix
    similarUsers=-1*np.ones((nUsers,k))
    
    similarities=cosine_similarity(r)
       
    # for each user
    for i in range(0, nUsers):
        simUsersIdxs= np.argsort(similarities[:,i])
        
        l=0
        #find its most similar users    
        for j in range(simUsersIdxs.size-2, simUsersIdxs.size-k-2,-1):
            simUsersIdxs[-k+1:]
            similarUsers[i,l]=simUsersIdxs[j]
            l=l+1
            
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
lower_limit = 150
upper_limit = 201

sql_users_in_recommender = """select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                              group by UserID having no_of_ratings > %s and no_of_ratings < %s LIMIT 2000000"""

cursor.execute(sql_users_in_recommender, (lower_limit, upper_limit))
results = cursor.fetchall()
results_users = [el[0] for el in [e for e in results]]
print(results_users)
results_users.sort()



sql_ISBN_in_recommender = """SELECT distinct ISBN from books.ratings_table where UserID in
                             (select distinct UserID from books.ratings_table group by UserID
                             having COUNT(*) > %s and COUNT(*) < %s) LIMIT 2000000"""
cursor.execute(sql_ISBN_in_recommender, (lower_limit, upper_limit))
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

similarUsers, similarities=findKSimilar (r,5)

# Evaluation
start = datetime.now()
mae=0
for i in range(0,nUsers):
    for j in range(0, nItems):
        rhat=predict (i,j,r, similarUsers, similarities)
        print (i, '-', j, 'prediction, real',rhat,r[i,j])
        if not np.isnan(rhat):
            mae=mae+np.abs(rhat-r[i,j])
print ('MAE=',mae)


print("Calculation took approximately: ", (datetime.now() - start).seconds, " seconds")



# Similar Users to CSV
columns_similar_users = ['similar1', 'similar2', 'similar3', 'similar4', 'similar5']
df_similar_users = pd.DataFrame(data = similarUsers, index = results_users, columns = columns_similar_users)

max_users_range = len(results_users) 
max_similar_range = 5 #k=5
for x in range(0, max_users_range):
    for y in range(0, max_similar_range):
        user = results_users[int(df_similar_users.iloc[x][y])]
        df_similar_users.iloc[x][y] = user
        
df_similar_users.to_csv("neighbors-k-books.csv", index=True, header=True, sep=';', encoding="ISO-8859-1")



# Similar users to db
similar_users_original_path = """neighbors-k-books.csv"""

# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root",
                     local_infile=True)

cursor = db.cursor()

wait_timeout = """SET innodb_lock_wait_timeout = 120"""
show_warnings = """SHOW warnings"""

# Settings
cursor.execute(wait_timeout)


destination_path = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books"""
copy_similar_users = shutil.copy(similar_users_original_path, destination_path)


cursor.execute("use books")

# Populate similar_users_table
populate_similar_users = """LOAD DATA LOW_PRIORITY INFILE 'neighbors-k-books.csv'
                            INTO TABLE books.user_neighbors
                            CHARACTER SET latin1
                            FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n'
                            IGNORE 1 LINES (`UserID`, `Similar1`, `Similar2`, `Similar3`, `Similar4`, `Similar5`)"""

cursor.execute(populate_similar_users)
db.commit()
cursor.execute(show_warnings)



# Close db connection
db.close()




df_similarities = pd.DataFrame(data = similarities, index = results_users, columns = results_users)

similarities_list = []
for x in range(0, max_users_range):
    for y in range(0, max_users_range):
        if round(df_similarities.iat[x,y],4) != 0:
            similarities_list.append([results_users[x], results_users[y], round(df_similarities.iat[x,y],4)])
            
columns_similarities_to_db = ["UserId", "SimilarUser", "Similarity"]
df_similarities_to_db = pd.DataFrame(similarities_list, columns = columns_similarities_to_db)

df_similarities_to_db.to_csv("user-pairs-books.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")

# User pairs to db
user_pairs_original_path = """user-pairs-books.csv"""

# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root",
                     local_infile=True)

cursor = db.cursor()

wait_timeout = """SET innodb_lock_wait_timeout = 120"""
show_warnings = """SHOW warnings"""

# Settings
cursor.execute(wait_timeout)


destination_path = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books"""
copy_user_pairs = shutil.copy(user_pairs_original_path, destination_path)

cursor.execute("use books")

# Populate user_pairs
populate_user_pairs = """LOAD DATA LOW_PRIORITY INFILE 'user-pairs-books.csv'
                          INTO TABLE books.user_pairs
                          CHARACTER SET latin1
                          FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                          IGNORE 1 LINES (`UserID`, `Similar`, `Similarity`)"""

cursor.execute(populate_user_pairs)
db.commit()
cursor.execute(show_warnings)



# Close db connection
db.close()