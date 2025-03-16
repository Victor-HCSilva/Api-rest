import mysql.connector
from mysql.connector import Error
import logging
import os
import sys

path_abs = os.path.abspath(os.curdir)
sys.path.insert(0, path_abs)
print(path_abs)

class DataBase:
    tableName = "booksdb"
    
    def __init__(self, host, database, user, password):
        self.conn = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                )
        self.cursor = self.conn.cursor()
        self.log = logging.getLogger(__name__)
        self.db = database

    def create_table(self):
        self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {self.tableName}(
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(400),
                                author VARCHAR(400),
                                age INT,
                                gender VARCHAR(100))""")
        self.conn.commit()   

    def add_new_book(self, name, author, age, gender):

        query = f"INSERT INTO {self.tableName} (name, author, age, gender) VALUES (%s, %s, %s, %s)"

        data = (name, author, age, gender)

        self.cursor.execute(query, data)

        self.conn.commit()


        return self.cursor.lastrowid
    
    def list_all(self):
        self.conn.cursor()
        self.cursor.execute(f" SELECT * FROM {self.tableName} ")
        return self.cursor.fetchall()

    def get_book(self, book_id):
        if book_id:
            self.cursor.execute(f"SELECT * FROM {self.tableName} WHERE id={book_id};")
           
                
            return self.cursor.fetchall()
        else:
            return
    
    def update_info(self,book_id, name, author, age, gender):
    
        query = f"UPDATE {self.tableName} SET name=%s, author=%s, age=%s, gender=%s WHERE id=%s"

        data = (name, author, age, gender,book_id)

        self.cursor.execute(query, data)

        self.conn.commit()


        return self.cursor.lastrowid
 

    def remove_book(self, book_id):
        if book_id:
            self.cursor.execute(f"DELETE FROM {self.tableName} WHERE id={book_id};")
            print("Objeto encontrado")
            self.conn.commit()
        else:
            print(f"Não existe livro com id {book_id}")
 
    def end_connect(self):
        self.cursor.close()
        self.conn.close()
        print("Conexao encerrada")

if __name__ == "__main__":
    ...
