import pymysql
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import shutil


# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root")

cursor = db.cursor()

cursor.execute("use books")

ratings_lower_limit = 150
retings_upper_limit = 501
age_lower_limit = 19
age_upper_limit = 41

sql_users_in_recommender = """select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                              group by UserID having no_of_ratings > %s and no_of_ratings < %s LIMIT 2000000"""
                              
sql_users_ages_in_recommender = """select UserID from 
	                               (select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                                   group by UserID having no_of_ratings > %s and no_of_ratings < %s LIMIT 2000000) as rband
	                               where rband.UserID in 
	                               (SELECT UserID FROM books.users_table where Age > %s and Age < %s)"""

cursor.execute(sql_users_ages_in_recommender, (ratings_lower_limit, retings_upper_limit, age_lower_limit, age_upper_limit))
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
