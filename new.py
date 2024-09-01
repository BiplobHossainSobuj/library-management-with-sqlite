import sqlite3
import csv
db = sqlite3.connect("practice.sqlite")
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS books (id INTEGER NOT NULL PRIMARY KEY,title TEXT NOT NULL,author TEXT NOT NULL,status INTEGER)")
db.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER NOT NULL PRIMARY KEY,name TEXT NOT NULL)")
db.execute("CREATE TABLE IF NOT EXISTS borrow_info (user_id INTEGER NOT NULL,book_id INTEGER NOT NULL,borrow_date DATE NOT NULL,PRIMARY KEY (user_id, book_id))")

class Library:
    
    def insert_book(self,book):
        with db:
            cursor.execute("INSERT INTO books VALUES (:id, :title, :author, :status)",{'id':book.id,'title':book.title,'author':book.author,'status':book.status})
    def delete_book(self,id):
        with db:
            cursor.execute("DELETE FROM books WHERE id=:id",{'id':id})

    def update_book(self,book):
        with db:
            cursor.execute("UPDATE books SET title=:title,author=:author,status=:status WHERE id=:id",{'id':book.id,'title':book.title,'author':book.author,'status':book.status})

    def search_book(self,title):
        with db:
            cursor.execute("SELECT * FROM books WHERE title=:title",{'title':title})
            return cursor.fetchone()
        
    def report(self):
        number_of_books = self.get_number_of_items('books')
        print(f'TOTAL BOOKS {number_of_books}')
        number_of_users = self.get_number_of_items('users')
        print(f'TOTAL USERS: {number_of_users}')
        
    def get_number_of_items(self,table_name):
        with db:
            cursor.execute(f"SELECT * FROM {table_name}")
            number_of_items = cursor.fetchall()
            return len(number_of_items)
    
    def add_user(self,user):
        with db:
            cursor.execute("INSERT INTO users VALUES (:id, :name)",{'id':user.id,'name':user.name})
            
    def delete_user(self,id):
        with db:
            cursor.execute("DELETE FROM users WHERE id=:id",{'id':id})
            
    def update_user(self,user):
        with db:
            cursor.execute("UPDATE users SET name=:name WHERE id=:id",{'id':user.id,'name':user.name})
    def export_to_csv(self):
        with db:
            cursor.execute(f"SELECT * FROM books")
            row = cursor.description
            column = [field[0] for field in row]
            with open('book.csv','w',newline='') as file:
                writer = csv.writer(file)
                writer.writerow(column)
                writer.writerows(cursor.fetchall())
class Book:
    
    def __init__(self,id,title,author,status=False) -> None:
            self.id = id
            self.title = title
            self.author = author
            self.status = status            

class User:
    
    def __init__(self,id,name) -> None:
        self.id = id
        self.name = name
        
    def borrow_book(self,id,borrow_date):
        with db:
            is_available = cursor.execute(f'SELECT status FROM books WHERE id={id}')
            if (is_available.fetchone()[0] == 1):
                cursor.execute("INSERT INTO borrow_info VALUES(:user_id,:book_id,:borrow_date)",{'book_id':id,'user_id':self.id,'borrow_date':borrow_date})
                cursor.execute("UPDATE books set status=:status WHERE id=:id",{'status':False,'id':id})
            else:
                print("The book is not available")
                
    def return_book(self,book_id):
        with db:
            is_available = cursor.execute(f'SELECT status FROM books WHERE id={book_id}')
            if (is_available.fetchone()[0] == 1):
                print("The book is not borrowed yet")
            else:
                cursor.execute("DELETE FROM borrow_info WHERE user_id=:user_id AND book_id=:book_id",{'book_id':book_id,'user_id':self.id})
                cursor.execute("UPDATE books set status=:status WHERE id=:id",{'status':True,'id':book_id})
                print("You have returned the book successfully")
     


def main():
    while True:
        user_id = int(input("Enter user id: "))
        user_name = str(input("Enter user name: "))
        user_pass = str(input("Enter Password: "))
        
        if user_name=='admin' and user_pass=='admin':
            choice=0
            while choice != 10:
                print("-----Welcome to the Library-----")
                print('1.Add book')
                print('2.Remove Book')
                print('3.Update Book')
                print('4.Search Book')
                print('5.Add User')
                print('6.Remove User')
                print('7.Update User')
                print('8.Usage Report')
                print('9.Export csv')
                print('10.Exit')
                choice = int(input('Enter a number between 1 to 10: '))
                Library1 = Library()
                if choice == 1:
                    print("------Add a new book-----")
                    id = int(input("Enter a book ID: "))
                    title = str(input("Enter title of the book: "))
                    author = str(input("Enter author of the book: "))
                    book = Book(id,title,author,True)
                    Library1.insert_book(book)
                if choice == 2:
                    id = int(input("Enter a book ID: "))
                    Library1.delete_book(id)
                if choice == 3:
                    print("------Update book -----")
                    id = int(input("Enter a book ID to be updated: "))
                    title = str(input("Enter title of the book: "))
                    author = str(input("Enter author of the book: "))
                    book = Book(id,title,author)
                    Library1.update_book(book)
                if choice == 4:
                    print("------Search book -----")
                    title = str(input("Enter title of the book: "))
                    book=Library1.search_book(title)
                    print("Search Result: ",book)
                if choice == 5:
                    print("-----Add User___")
                    id = int(input("Enter user Id: "))
                    name = str(input("Enter user Name: "))
                    user = User(id,name)
                    Library1.add_user(user)
                if choice == 6:
                    print("Remove User")
                    id = int(input("Enter user id: "))
                    Library1.delete_user(id)
                if choice == 7:
                    print("Update User")
                    id = int(input("Enter user Id: "))
                    name = str(input("Enter user Name: "))
                    user = User(id,name)
                    Library1.update_user(user)
                if choice == 8:
                    print("----Usage Report-----")
                    Library1.report()
                if choice == 9:
                    exported = Library1.export_to_csv()
                    if exported:
                        print("The file as exported book.csv")
        else:
            print("Welcome to library")
            user = User(user_id,user_name)
            choice = 0
            while choice != 3:
                print("1.Borrow Book")
                print("2.Return Book")
                choice = int(input("Select you choice: "))
                
                if choice == 1:
                    book_id = int(input("Enter book id: "))
                    borrow_date = str(input("Enter Date: "))
                    user.borrow_book(book_id,borrow_date)
                elif choice == 2:
                    book_id = int(input("Enter book id: "))
                    user.return_book(book_id)
                else:
                    break
    else:
        print("Something went wrong")           
if __name__ == '__main__':
    main()
    db.close()