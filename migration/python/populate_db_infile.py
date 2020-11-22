import pymysql

show_wornings = """SHOW warnings"""
    

# Open db connection
db = pymysql.connect(host = "localhost",
                     user = "root",
                     passwd = "root",
                     local_infile = True)
cursor = db.cursor()
cursor.execute("SET innodb_lock_wait_timeout = 120")
cursor.execute("use books")



# Populate books_table
populate_books = """LOAD DATA LOW_PRIORITY INFILE 'books_to_db.csv'
                    INTO TABLE books.books_table
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                    IGNORE 1 LINES (`ISBN`, `Book-Title`, `Book-Author`, `year`, `Publisher`)"""

cursor.execute(populate_books)
db.commit()
cursor.execute(show_wornings)


# Populate users
populate_users = """LOAD DATA LOW_PRIORITY INFILE 'users_to_db.csv'
                    INTO TABLE books.users
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n'
                    IGNORE 1 LINES (`userid`, `location`, `age`)"""
                    
cursor.execute(populate_users)
db.commit()
cursor.execute(show_wornings)


# Populate ratings_table
populate_ratings = """LOAD DATA LOW_PRIORITY INFILE 'ratings_to_db.csv'
                      INTO TABLE books.ratings_table
                      CHARACTER SET latin1
                      FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n'
                      IGNORE 1 LINES (`User-ID`, `ISBN`, `Book-Rating`)"""
                     
cursor.execute(populate_ratings)
db.commit()
cursor.execute(show_wornings)

# Close db connection
db.close()