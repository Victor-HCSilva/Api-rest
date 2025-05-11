from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database as db
import os
import sys
from fastapi.middleware.cors import CORSMiddleware

path_abs = os.path.abspath(os.curdir)
sys.path.insert(0, path_abs)
app = FastAPI()

origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "http://10.0.0.100:8080", # <-- ADICIONE ESTA LINHA
    # "*" # Cuidado ao usar o wildcard
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/")
async def get_book(book_id):
    book = db.DataBase(
        host="localhost", database="library", user="root", password="senha"
    )
    book.create_table()
    data = book.get_book(book_id)[0]
    book_format ={ "id":data[0], "name":data[1], "author": data[2], "age":data[3], "gender":data[4]}

    return  book_format

@app.get("/api/all")
async def list_all():
    books = db.DataBase(
        host="localhost", database="library", user="root", password="senha"
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
        host="localhost", database="library", user="root", password="senha"
    )

    new_book.create_table()
    new_book.add_new_book(name=name, author=author, age=age, gender=gender)

    book_format ={"name":name, "author": author, "age":age, "gender":gender}

    return  book_format

@app.put("/api/update")
async def update(name: str, author: str, age: str, gender: str, book_id: str):
    new_book = db.DataBase(
        host="localhost", database="library", user="root", password="senha"
    )
    new_book.create_table()
    new_book.update_info(
        name=name, author=author, age=age, gender=gender, book_id=book_id
    )
    return {"message":"Update"}

@app.delete("/api/delete")
async def remove(book_id):
    book = db.DataBase(
        host="localhost", database="library", user="root", password="senha"
    )
    book.remove_book(book_id)
    return {"message":"Book deleted."}
