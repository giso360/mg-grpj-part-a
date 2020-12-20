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






def find_recommended_books(userid):
    recommended_books = []
    
    db = pymysql.connect(host = "localhost",
                      user = "root",
                      passwd = "root")
    cursor = db.cursor()
    cursor.execute("use books")
    
    
    get_similar_users = """SELECT * FROM books.user_neighbors_age where UserId = %s"""
    cursor.execute(get_similar_users, (userid))
    result_get_similar_users = list(cursor.fetchall())
    similar_users = [list(i) for i in result_get_similar_users]
    similar_users_list = []
    similar_users_list = [item for sublist in similar_users for item in sublist]
    similar_users_list = similar_users_list[1:]
    
    users_books = []
    get_users_books = """SELECT * from books.ratings_table where UserId = %s"""
    cursor.execute(get_users_books, (userid))
    result_get_users_books = list(cursor.fetchall())
    for record in result_get_users_books:
        users_books.append(record[2])
        
    book_rating = 7
    books = []
    get_books = """SELECT * FROM books.ratings_table where UserId = %s and BookRating > %s"""
    for i in range (0, len(similar_users_list)):
        cursor.execute(get_books, (similar_users_list[i], book_rating))
        result_get_books = list(cursor.fetchall())
        for record in result_get_books:
            books.append(record[2])
            
    books = set(books)
    recommended_books = [book for book in books if book not in users_books]
    
    print("Recomended Books: ")
    get_book_name = """SELECT * FROM books.books_table where ISBN = %s"""
    for book in recommended_books:
        cursor.execute(get_book_name, (book))
        result_get_book_name = list(cursor.fetchall())
        for record in result_get_book_name:
            print(record[0], ": ", record[1])
    # Close db connection
    db.close()
    return








# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root")

cursor = db.cursor()

cursor.execute("use books")

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

# # Close db connection
db.close()


df_for_recommender = pd.read_csv("../ratings_to_db.csv", sep=";", encoding="ISO-8859-1")
df_for_recommender = df_for_recommender[df_for_recommender["User-ID"].isin(results_users)]
print(df_for_recommender.shape)
print("the recommender focuses on number of ratings for the prescribed bin: ", df_for_recommender.shape[0])
print("Ratings for number of users: ", df_for_recommender["User-ID"].nunique())

df = pd.DataFrame(index = results_users, columns = results_ISBN)

for index, row in df_for_recommender.iterrows():
    df.loc[row['User-ID'], row['ISBN']] = row['Book-Rating']
    
df = df.fillna(value = 0)  



# Recommender
nUsers = len(results_users)
nItems = len(results_ISBN)
r = df.to_numpy()


similarUsers, similarities=findKSimilar (r,k)

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

# Similar Users to CSV
columns_similar_users = ['similar1', 'similar2', 'similar3', 'similar4', 'similar5']
df_similar_users = pd.DataFrame(data = similarUsers, index = results_users, columns = columns_similar_users)


max_users_range = len(results_users) 
max_similar_range = k #k=5
for x in range(0, max_users_range):
    for y in range(0, max_similar_range):
        user = results_users[int(df_similar_users.iloc[x][y])]
        df_similar_users.iloc[x][y] = user
        
df_similar_users.to_csv("neighbors-ages-k-books.csv", index=True, header=True, sep=';', encoding="ISO-8859-1")

# Similar users to db
similar_users_original_path = """neighbors-ages-k-books.csv"""

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
populate_similar_users = """LOAD DATA LOW_PRIORITY INFILE 'neighbors-ages-k-books.csv'
                            INTO TABLE books.user_neighbors_age
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
df_similarities_to_db.to_csv("user-pairs-ages-books.csv", index=False, header=True, sep=';', encoding="ISO-8859-1")
# User pairs to db
user_pairs_original_path = """user-pairs-ages-books.csv"""

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
populate_user_pairs = """LOAD DATA LOW_PRIORITY INFILE 'user-pairs-ages-books.csv'
                          INTO TABLE books.user_pairs_age
                          CHARACTER SET latin1
                          FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                          IGNORE 1 LINES (`UserID`, `Similar`, `Similarity`)"""

cursor.execute(populate_user_pairs)
db.commit()
cursor.execute(show_warnings)

# Close db connection
db.close()



books = find_recommended_books(276994)