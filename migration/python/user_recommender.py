import pymysql

def find_recommended_books(userid):
    recommended_books = []
    
    db = pymysql.connect(host = "localhost",
                      user = "root",
                      passwd = "root")
    cursor = db.cursor()
    cursor.execute("use books")
    
    
    get_similar_users = """SELECT * FROM books.user_neighbors where UserId = %s"""
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

books = find_recommended_books(276994)
# books = find_recommended_books(244309)