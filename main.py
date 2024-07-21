# Developed By : <PRIYANSHUL SHARMA>
# My blog https://priyanshul.is-a.dev/


import mysql.connector as pymysql
from datetime import datetime

passwrd = None
db = None  
C = None

def base_check():
    check = 0
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'library':
                cursor.execute('USE library')
                check = 1
    if check != 1:
        create_database()

def table_check():
    db = pymysql.connect(host="localhost", user="root", password=passwrd)
    cursor = db.cursor()
    cursor.execute('SHOW DATABASES')
    result = cursor.fetchall()
    for r in result:
        for i in r:
            if i == 'library':
                cursor.execute('USE library')
                cursor.execute('SHOW TABLES')
                result = cursor.fetchall()
                if len(result) <= 2:
                    create_tables()
                else:
                    print('      Booting systems...')

def create_database():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd)
        cursor = db.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS library")
        db.commit()
        db.close()
        print("Database 'library' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating database: {str(e)}")

def create_tables():
    try:
        db = pymysql.connect(host="localhost", user="root", password=passwrd, database="library")
        cursor = db.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS books (
                BOOK_ID INT PRIMARY KEY,
                TITLE VARCHAR(255),
                AUTHOR VARCHAR(255),
                YEAR INT,
                AVAILABLE INT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                USER_ID INT PRIMARY KEY,
                NAME VARCHAR(255),
                PHONE_NO VARCHAR(15)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                TRANSACTION_ID INT AUTO_INCREMENT PRIMARY KEY,
                USER_ID INT,
                BOOK_ID INT,
                ISSUE_DATE DATE,
                RETURN_DATE DATE,
                FOREIGN KEY (USER_ID) REFERENCES users(USER_ID),
                FOREIGN KEY (BOOK_ID) REFERENCES books(BOOK_ID)
            )
        """)
        
        db.commit()
        db.close()
        print("Tables 'books', 'users', and 'transactions' created successfully.")
    except pymysql.Error as e:
        print(f"Error creating tables: {str(e)}")

def QR():
    result = C.fetchall()
    for r in result:
        print(r)

def add_book():
    book_id = int(input("Enter Book ID: "))
    title = input("Enter Book Title: ")
    author = input("Enter Author: ")
    year = int(input("Enter Year of Publication: "))
    available = int(input("Enter Number of Available Copies: "))
    data = (book_id, title, author, year, available)
    sql = "INSERT INTO books (BOOK_ID, TITLE, AUTHOR, YEAR, AVAILABLE) VALUES (%s, %s, %s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('Book added successfully...')
    except pymysql.Error as e:
        print(f"Error adding book: {str(e)}")

def view_books():
    C.execute("SELECT * FROM books")
    QR()

def update_book():
    book_id = int(input("Enter Book ID to update: "))
    field = input("Enter field to update [TITLE, AUTHOR, YEAR, AVAILABLE]: ")
    new_value = input(f"Enter new value for {field}: ")
    if field in ['YEAR', 'AVAILABLE']:
        new_value = int(new_value)
    sql = f"UPDATE books SET {field} = %s WHERE BOOK_ID = %s"
    try:
        C.execute(sql, (new_value, book_id))
        db.commit()
        print('Book updated successfully...')
    except pymysql.Error as e:
        print(f"Error updating book: {str(e)}")

def delete_book():
    book_id = int(input("Enter Book ID to delete: "))
    sql = "DELETE FROM books WHERE BOOK_ID = %s"
    try:
        C.execute(sql, (book_id,))
        db.commit()
        print('Book deleted successfully...')
    except pymysql.Error as e:
        print(f"Error deleting book: {str(e)}")

def register_user():
    user_id = int(input("Enter User ID: "))
    name = input("Enter User Name: ")
    phone_no = input("Enter User Phone Number: ")
    data = (user_id, name, phone_no)
    sql = "INSERT INTO users (USER_ID, NAME, PHONE_NO) VALUES (%s, %s, %s)"
    try:
        C.execute(sql, data)
        db.commit()
        print('User registered successfully...')
    except pymysql.Error as e:
        print(f"Error registering user: {str(e)}")

def view_users():
    C.execute("SELECT * FROM users")
    QR()

def issue_book():
    user_id = int(input("Enter User ID: "))
    book_id = int(input("Enter Book ID: "))
    issue_date = datetime.now().date()
    sql_check = "SELECT AVAILABLE FROM books WHERE BOOK_ID = %s"
    C.execute(sql_check, (book_id,))
    result = C.fetchone()
    if result and result[0] > 0:
        sql_issue = "INSERT INTO transactions (USER_ID, BOOK_ID, ISSUE_DATE) VALUES (%s, %s, %s)"
        try:
            C.execute(sql_issue, (user_id, book_id, issue_date))
            sql_update = "UPDATE books SET AVAILABLE = AVAILABLE - 1 WHERE BOOK_ID = %s"
            C.execute(sql_update, (book_id,))
            db.commit()
            print('Book issued successfully...')
        except pymysql.Error as e:
            print(f"Error issuing book: {str(e)}")
    else:
        print("Book not available.")

def return_book():
    user_id = int(input("Enter User ID: "))
    book_id = int(input("Enter Book ID: "))
    return_date = datetime.now().date()
    sql_update = "UPDATE transactions SET RETURN_DATE = %s WHERE USER_ID = %s AND BOOK_ID = %s AND RETURN_DATE IS NULL"
    try:
        C.execute(sql_update, (return_date, user_id, book_id))
        sql_check = "SELECT ISSUE_DATE FROM transactions WHERE USER_ID = %s AND BOOK_ID = %s AND RETURN_DATE = %s"
        C.execute(sql_check, (user_id, book_id, return_date))
        result = C.fetchone()
        if result:
            sql_book = "UPDATE books SET AVAILABLE = AVAILABLE + 1 WHERE BOOK_ID = %s"
            C.execute(sql_book, (book_id,))
            db.commit()
            print('Book returned successfully...')
        else:
            print("Transaction not found or already returned.")
    except pymysql.Error as e:
        print(f"Error returning book: {str(e)}")

def main():
    global passwrd
    passwrd = input("Enter password for MySQL: ")

    base_check()

    table_check()
    
    global db, C
    db = pymysql.connect(host="localhost", user="root", password=passwrd, database="library")
    C = db.cursor()
    while True:
        log = input("For Admin: A, For Librarian: L ::: ")
        if log.upper() == "A":
            p = input("ENTER ADMIN PASSWORD: ")
            if p == 'admin123':
                print("LOGIN SUCCESSFUL")
                while True:
                    menu = input('''Add Book: AB, View Books: VB, Update Book: UB, Delete Book: DB, Register User: RU, View Users: UV, Issue Book: IB, Return Book: RB, Exit: X :::''')
                    if menu.upper() == 'AB':
                        add_book()
                    elif menu.upper() == 'VB':
                        view_books()
                    elif menu.upper() == 'UB':
                        update_book()
                    elif menu.upper() == 'DB':
                        delete_book()
                    elif menu.upper() == 'RU':
                        register_user()
                    elif menu.upper() == 'UV':
                        view_users()
                    elif menu.upper() == 'IB':
                        issue_book()
                    elif menu.upper() == 'RB':
                        return_book()
                    elif menu.upper() == 'X':
                        break
                    else:
                        print("Wrong Input")
                        
        elif log.upper() == "L":
            print("Librarian Interface")
            while True:
                menu = input('''Issue Book: IB, Return Book: RB, Exit: X :::''')
                if menu.upper() == 'IB':
                    issue_book()
                elif menu.upper() == 'RB':
                    return_book()
                elif menu.upper() == 'X':
                    break
                else:
                    print("Wrong Input")

if __name__ == "__main__":
    main()
