import pymysql
import shutil


# File's original paths
books_original_path = """../books_to_db.csv"""
users_original_path = """../users_to_db.csv"""
ratings_original_path = """../ratings_to_db.csv"""


# MySQL queries
show_warnings = """SHOW warnings"""
get_path = """SELECT @@datadir"""
wait_timeout = """SET innodb_lock_wait_timeout = 120"""
use_db = """use books"""


# Open db connection
db = pymysql.connect(host = "localhost",
                     user = "root",
                     passwd = "root",
                     local_infile = True)
cursor = db.cursor()


# Settings
cursor.execute(wait_timeout)


# Get path
cursor.execute(get_path)
# destination_path = [item[0] for item in cursor.fetchall()]
destination_path = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books"""

copy_books = shutil.copy(books_original_path, destination_path)
copy_users = shutil.copy(users_original_path, destination_path)
copy_ratings = shutil.copy(ratings_original_path, destination_path)


# Use database
cursor.execute(use_db)

# Populate books_table
populate_books = """LOAD DATA LOW_PRIORITY INFILE 'books_to_db.csv'
                    INTO TABLE books.books_table
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                    IGNORE 1 LINES (`ISBN`, `Book-Title`, `Book-Author`, `year`, `Publisher`)"""

cursor.execute(populate_books)
db.commit()
cursor.execute(show_warnings)


# Populate users
populate_users = """LOAD DATA LOW_PRIORITY INFILE 'users_to_db.csv'
                    INTO TABLE books.users
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n'
                    IGNORE 1 LINES (`userid`, `location`, `age`)"""
                    
cursor.execute(populate_users)
db.commit()
cursor.execute(show_warnings)


# Populate ratings_table
populate_ratings = """LOAD DATA LOW_PRIORITY INFILE 'ratings_to_db.csv'
                      INTO TABLE books.ratings_table
                      CHARACTER SET latin1
                      FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\n'
                      IGNORE 1 LINES (`User-ID`, `ISBN`, `Book-Rating`)"""
                     
cursor.execute(populate_ratings)
db.commit()
cursor.execute(show_warnings)

# Close db connection
db.close()