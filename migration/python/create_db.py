import pymysql

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
                 `Book-Title` varchar(300) DEFAULT 'UNKNOWN TITLE',
                 `Book-Author` varchar(150) DEFAULT 'UNKNOWN AUTHOR',
                 `year` year(4) DEFAULT '0000',
                 `Publisher` varchar(300) DEFAULT 'UNKNOWN PUBLISHER',
                 PRIMARY KEY (`ISBN`),
                 UNIQUE KEY `isbn_UNIQUE` (`ISBN`)
                 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(books_char)
cursor.execute(books_table)

# Create users
users_char = """SET character_set_client = utf8mb4"""
users_table = """CREATE TABLE `users` (
                 `userid` int(11) NOT NULL,
                 `location` varchar(45) DEFAULT 'UNKNOWN COUNTRY',
                 `age` int(11) DEFAULT NULL,
                 PRIMARY KEY (`userid`)
                 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(users_char)
cursor.execute(users_table)

# Create ratings_table
ratings_char = """SET character_set_client = utf8mb4"""
ratings_table = """CREATE TABLE `ratings_table` (
                   `ratingid` int(11) NOT NULL AUTO_INCREMENT,
                   `User-ID` int(11) NOT NULL,
                   `ISBN` varchar(45) NOT NULL,
                   `Book-Rating` int(11) NOT NULL,
                   PRIMARY KEY (`ratingid`)
                   ) ENGINE=InnoDB AUTO_INCREMENT=3640120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci"""
cursor.execute(ratings_char)
cursor.execute(ratings_table)

# Close db connection
db.close()