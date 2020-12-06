import pymysql

# Open database connection
db = pymysql.connect(host="localhost",
                     user="root",
                     passwd="root")

cursor = db.cursor()

cursor.execute("use books")


select_all = """SELECT * FROM books.ratings_table"""


count_all = """SELECT count(*) FROM books.ratings_table"""
cursor.execute(count_all)
result_count_all = list(cursor.fetchall())
print(result_count_all[0][0])


select_userid = """select UserID from books.ratings_table"""
cursor.execute(select_userid)
result_select_userid = list(cursor.fetchall())
print(result_select_userid[:20])
all_userid = []
for record in result_select_userid:
    all_userid.append(record[0])
print(all_userid[:20])


count_distinct_userid = """select count(distinct UserID) from books.ratings_table"""
cursor.execute(count_distinct_userid)
result_count_distinct_userid = list(cursor.fetchall())
print(result_count_distinct_userid)
number_unique_userid = result_count_distinct_userid[0][0]
print(number_unique_userid)


select_userid_276762 = """select * from books.ratings_table where UserID = 276762"""
cursor.execute(select_userid_276762)
result_select_userid_276762 = list(cursor.fetchall())
# print(result_select_userid_276762[1][0])
print(result_select_userid_276762)
# turn into list
ratingid = []
for record in result_select_userid_276762:
    ratingid.append(record[0])
print(ratingid)


count_userid_276762 = """select UserID, COUNT(*) from books.ratings_table where UserID = 276762"""
cursor.execute(count_userid_276762)
result_count_userid_276762  = list(cursor.fetchall())
print(result_count_userid_276762)
number_of_ratings_userid_276762 = result_count_userid_276762[0][1]
print(number_of_ratings_userid_276762)


userid_number_of_ratings_under_150 = """select distinct UserID, COUNT(*) as no_of_ratings
                                        from books.ratings_table group by UserID
                                        having no_of_ratings < 150 LIMIT 2000000"""
cursor.execute(userid_number_of_ratings_under_150)
result_userid_number_of_ratings_under_150 = list(cursor.fetchall())
print(result_userid_number_of_ratings_under_150[:20])

list_userid_number_of_ratings_under_150 = []
for record in result_userid_number_of_ratings_under_150:
    list_userid_number_of_ratings_under_150.append(record[0])
print(list_userid_number_of_ratings_under_150[:20])


number_of_users_with_ratings_1 = """select Count(*) from (select distinct UserID, COUNT(*) as no_of_ratings
                                            from books.ratings_table group by UserID having no_of_ratings > 150
                                            LIMIT 2000000) AS ag"""
cursor.execute(number_of_users_with_ratings_1)
result_number_of_users_with_ratings_1 = list(cursor.fetchall())
print(result_number_of_users_with_ratings_1)
int_result_number_of_users_with_ratings_1 = result_number_of_users_with_ratings_1[0][0]
print(int_result_number_of_users_with_ratings_1)


userid_with_ratings_1 = """select distinct UserID, COUNT(*) as no_of_ratings from books.ratings_table
                            group by UserID having no_of_ratings = 1 LIMIT 2000000"""
cursor.execute(userid_with_ratings_1)
result_userid_with_ratings_1 = list(cursor.fetchall())
print(result_userid_with_ratings_1[:20])

list_userid_with_ratings_1 = []
for record in result_userid_with_ratings_1:
    list_userid_with_ratings_1.append(record[0])
print(list_userid_with_ratings_1[:20])


userid_number_of_ratings_under_6 = """select distinct UserID, COUNT(*) as no_of_ratings
                                      from books.ratings_table group by UserID
                                      having no_of_ratings < 6 LIMIT 2000000"""
cursor.execute(userid_number_of_ratings_under_6)
result_userid_number_of_ratings_under_6 = list(cursor.fetchall())
print(result_userid_number_of_ratings_under_6[:20])
list_result_userid_number_of_ratings_under_6 = []
for record in result_userid_number_of_ratings_under_6:
    list_result_userid_number_of_ratings_under_6.append(record[0])
print(list_result_userid_number_of_ratings_under_6[:20])


# Close db connection
db.close()