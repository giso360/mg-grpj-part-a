import pymysql

show_variables = """SHOW VARIABLES LIKE '%LOCAL%'"""
set_global = """SET GLOBAL local_infile=1"""
show_wornings = """SHOW warnings"""
    

# Open db connection
db = pymysql.connect(host = "localhost",
                     user = "root",
                     passwd = "root")
cursor = db.cursor()

cursor.execute("use books")

# Populate books_table
populate_books = """LOAD DATA LOW_PRIORITY LOCAL INFILE 'C:\\Users\\George\\DataScience_MSc\\modules\\6001_IntroductionToBigData\\groupProject\\Part_A_Batch\\mg-grpj-part-a\\migration\\books_to_db.csv'
                    INTO TABLE `books`.`books_table`
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                    IGNORE 1 LINES
                    (`ISBN`, `Book-Title`, `Book-Author`, `year`, `Publisher`)"""

cursor.execute(show_variables)
cursor.execute(set_global)
cursor.execute(show_variables)
cursor.execute(populate_books)
db.commit()
cursor.execute(show_wornings)


# # Populate users
populate_users = """LOAD DATA LOW_PRIORITY LOCAL INFILE 'C:\\Users\\George\\DataScience_MSc\\modules\\6001_IntroductionToBigData\\groupProject\\Part_A_Batch\\mg-grpj-part-a\\migration\\users_to_db.csv'
                    INTO TABLE `books`.`users`
                    CHARACTER SET latin1
                    FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                    IGNORE 1 LINES
                    (`userid`, `location`, `age`"""
cursor.execute(show_variables)
cursor.execute(set_global)
cursor.execute(show_variables)
cursor.execute(populate_users)
db.commit()
cursor.execute(show_wornings)


# # Populate ratings_table
populate_ratings = """LOAD DATA LOW_PRIORITY LOCAL INFILE 'C:\\Users\\George\\DataScience_MSc\\modules\\6001_IntroductionToBigData\\groupProject\\Part_A_Batch\\mg-grpj-part-a\\migration\\ratings_to_db.csv'
                      INTO TABLE `books`.`ratings_table`
                      CHARACTER SET latin1
                      FIELDS TERMINATED BY ';' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '"' LINES TERMINATED BY '\r\n'
                      IGNORE 1 LINES
                      (`User-ID`, `ISBN`, `Book-Rating`)"""
                     
cursor.execute(show_variables)
cursor.execute(set_global)
cursor.execute(show_variables)
cursor.execute(populate_ratings)
db.commit()
cursor.execute(show_wornings)


# Close db connection
db.close()