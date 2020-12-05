import pymysql
import matplotlib.pyplot as plt

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
db.close()

plt.bar(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.values()), align='center')
plt.xticks(range(len(bins_and_number_of_ratings)), list(bins_and_number_of_ratings.keys()))