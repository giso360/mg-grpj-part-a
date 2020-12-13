import os
import pymysql

# Delete files before recreate DB
books_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/books_to_db.csv"""
users_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/users_to_db.csv"""
ratings_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/ratings_to_db.csv"""
similar_users_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/neighbors-k-books.csv"""
user_pairs_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/user-pairs-books.csv"""
similar_users_ages_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/neighbors-ages-k-books.csv"""
user_pairs_ages_file = """C:/ProgramData/MySQL/MySQL Server 8.0/Data/books/user-pairs-ages-books.csv"""

if os.path.isfile(books_file):
    os.remove(books_file)
    
if os.path.isfile(users_file):
    os.remove(users_file)
    
if os.path.isfile(ratings_file):
    os.remove(ratings_file)
    
if os.path.isfile(similar_users_file):
    os.remove(similar_users_file)
    
if os.path.isfile(user_pairs_file):
    os.remove(user_pairs_file)
    
if os.path.isfile(similar_users_ages_file):
    os.remove(similar_users_ages_file)
    
if os.path.isfile(user_pairs_ages_file):
    os.remove(user_pairs_ages_file)


# Open db connection
db = pymysql.connect(host = "localhost",
                      user = "root",
                      passwd = "root")
cursor=db.cursor()

# Delete already existing db
cursor.execute("DROP DATABASE IF EXISTS books")

# Create db
cursor.execute("create database books")
cursor.execute("use books")
cursor.execute("SET NAMES utf8")

# Create books_table
books_char = """SET character_set_client = utf8mb4"""
books_table = """CREATE TABLE `books_table` (
                 `ISBN` varchar(25) NOT NULL,
                 `BookTitle` varchar(300) DEFAULT 'UNKNOWN TITLE',
                 `BookAuthor` varchar(150) DEFAULT 'UNKNOWN AUTHOR',
                 `Year` int (4) DEFAULT '0000',
                 `Publisher` varchar(300) DEFAULT 'UNKNOWN PUBLISHER',
                 PRIMARY KEY (`ISBN`),
                 UNIQUE KEY `isbn_UNIQUE` (`ISBN`)
                 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(books_char)
cursor.execute(books_table)

# Create users
users_char = """SET character_set_client = utf8mb4"""
users_table = """CREATE TABLE `users_table` (
                 `UserId` int(11) NOT NULL,
                 `Location` varchar(45) DEFAULT 'UNKNOWN COUNTRY',
                 `Age` int(11) DEFAULT NULL,
                 PRIMARY KEY (`UserId`)
                 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(users_char)
cursor.execute(users_table)

# Create ratings_table
ratings_char = """SET character_set_client = utf8mb4"""
ratings_table = """CREATE TABLE `ratings_table` (
                   `RatingId` int(11) NOT NULL AUTO_INCREMENT,
                   `UserID` int(11) NOT NULL,
                   `ISBN` varchar(45) NOT NULL,
                   `BookRating` int(11) NOT NULL,
                   PRIMARY KEY (`RatingId`)
                   ) ENGINE=InnoDB AUTO_INCREMENT=3640120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(ratings_char)
cursor.execute(ratings_table)

# Create similar_users_table
similar_users_char = """SET character_set_client = utf8mb4"""
similar_users_table = """CREATE TABLE `user_neighbors`(
                         `UserId` int(11) NOT NULL,
                         `Similar1` int(11) NOT NULL,
                         `Similar2` int(11) NOT NULL,
                         `Similar3` int(11) NOT NULL,
                         `Similar4` int(11) NOT NULL,
                         `Similar5` int(11) NOT NULL,
                        PRIMARY KEY (`UserId`)
                        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
        
cursor.execute(similar_users_char)
cursor.execute(similar_users_table)

# Create similar_users_table
similar_users_age_char = """SET character_set_client = utf8mb4"""
similar_users_age_table = """CREATE TABLE `user_neighbors_age`(
                             `UserId` int(11) NOT NULL,
                             `Similar1` int(11),
                             `Similar2` int(11),
                             `Similar3` int(11),
                             `Similar4` int(11),
                             `Similar5` int(11),
                             PRIMARY KEY (`UserId`)
                             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
        
cursor.execute(similar_users_age_char)
cursor.execute(similar_users_age_table)
    
# Create user_pairs
user_pairs_char = """SET character_set_client = utf8mb4"""
user_pairs_table = """CREATE TABLE `user_pairs`(
                      `PairId` int(11) NOT NULL AUTO_INCREMENT,
                      `UserId` int(11) NOT NULL,
                      `Similar` int(11) NOT NULL,
                      `Similarity` DOUBLE NOT NULL,
                      PRIMARY KEY (`PairId`)
                      ) ENGINE=InnoDB AUTO_INCREMENT=3640120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
    
cursor.execute(user_pairs_char)
cursor.execute(user_pairs_table)

# Create user_pairs_age
user_pairs_age_char = """SET character_set_client = utf8mb4"""
user_pairs_age_table = """CREATE TABLE `user_pairs_age`(
                          `PairId` int(11) NOT NULL AUTO_INCREMENT,
                          `UserId` int(11) NOT NULL,
                          `Similar` int(11) NOT NULL,
                          `Similarity` DOUBLE NOT NULL,
                          PRIMARY KEY (`PairId`)
                          ) ENGINE=InnoDB AUTO_INCREMENT=3640120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
    
cursor.execute(user_pairs_age_char)
cursor.execute(user_pairs_age_table)

# Close db connection
db.close()