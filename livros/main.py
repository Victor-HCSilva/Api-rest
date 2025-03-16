from fastapi import FastAPI
from  pydantic import BaseModel
import database as db
import os
import sys

path_abs = os.path.abspath(os.curdir)
sys.path.insert(0, path_abs)
app = FastAPI()

@app.get("/api/")
async def get_book(book_id):
    book = db.DataBase(host = "localhost", database = "library", user= "root", password="senha")
    book.create_table()
    return book.get_book(book_id)

@app.get("/api/list")
async def get_all():
    books = db.DataBase(host = "localhost", database = "library", user= "root", password="senha")
    books.create_table()
    return books.list_all()

@app.post("/api/")
async def insert(name:str , author:str , age:str , gender:str):
    new_book = db.DataBase(host = "localhost", database = "library", user= "root", password="senha")
    new_book.create_table()
    new_book.add_new_book(name=name, author=author, age=age, gender=gender)
   
@app.put("/api/")
async def update_info(name:str , author:str , age:str , gender:str, book_id:str):
    new_book = db.DataBase(host = "localhost", database = "library", user= "root", password="senha")
    new_book.create_table()
    new_book.update_info(name=name, author=author, age=age, gender=gender, book_id=book_id)
 
@app.delete("/api/remove")
async def remove(book_id):
    book = db.DataBase(host = "localhost", database = "library", user= "root", password="senha")
    return book.remove_book(book_id)



