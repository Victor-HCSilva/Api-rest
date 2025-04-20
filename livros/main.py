from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database as db
import os
import sys

path_abs = os.path.abspath(os.curdir)
sys.path.insert(0, path_abs)
app = FastAPI()

@app.get("/api/")
async def get_book(book_id):
    book = db.DataBase(
        host="localhost", database="library", user="root", password="password"
    )
    book.create_table()
    return book.get_book(book_id)

@app.get("/api/all")
async def list_all():
    books = db.DataBase(
        host="localhost", database="library", user="root", password="password"
    )
    books.create_table()
    return books.list_all()

@app.post("/api/add")
async def new_book(name: str, author: str, age: str, gender: str):
    validation = {
            "name":name,
            "author":author,
            "gender":gender,
            }
    try:
        number_validation = int(age)
        if number_validation <=200 and number_validation > 2025:
            raise HTTPException(status_code=400, detail="Item age não pode ser negativo")
    except:
        raise HTTPException(status_code=400, detail="Erro no parâmetro age, deve ser número")
        return f"Age: {age}"

    for k,v in validation.items():
        if len(v) < 3:
            raise HTTPException(status_code=400, detail=f'Erro: parâmetro "{k}" muito curto')
            return f"{v}"

    new_book = db.DataBase(
        host="localhost", database="library", user="root", password="password"
    )
    new_book.create_table()
    new_book.add_new_book(name=name, author=author, age=age, gender=gender)

@app.put("/api/update")
async def update(name: str, author: str, age: str, gender: str, book_id: str):
    new_book = db.DataBase(
        host="localhost", database="library", user="root", password="password"
    )
    new_book.create_table()
    new_book.update_info(
        name=name, author=author, age=age, gender=gender, book_id=book_id
    )

@app.delete("/api/delete")
async def remove(book_id):
    book = db.DataBase(
        host="localhost", database="library", user="root", password="password"
    )
    return book.remove_book(book_id)
