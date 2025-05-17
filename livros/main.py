from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import database as db
import os
from fastapi.middleware.cors import CORSMiddleware
import datetime
from utils import check_, contains
from dotenv import load_dotenv


load_dotenv()

origins = [
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8080",
    "http://10.0.0.100:8080", # <-- ADICIONE ESTA LINHA
    # "*" # Cuidado ao usar o wildcard
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/get")
async def get_book(book_id:int):
    book = db.DataBase(
        host=os.getenv("HOST_NAME"), database="library", user=os.getenv("USER_NAME"), password=os.getenv("PASSWORD")
    )

    try:
        data = book.get_book(book_id)[0]

        book_format ={ "id":data[0], "name":data[1], "author": data[2], "age":data[3], "gender":data[4]}
        return  book_format
    except IndexError:
        raise HTTPException(status_code=404, detail=f"Livro com ID: {book_id} não encontrado.")

@app.get("/api/getall")
async def list_all():
    books = db.DataBase(
        host=os.getenv("HOST_NAME"), database="library", user=os.getenv("USER_NAME"), password=os.getenv("PASSWORD")
    )
    return books.list_all()

@app.post("/api/post")
async def new_book(name: str, author: str, age: int, gender: str):
    ano_atual = datetime.date.today().year
    validation = {
            "name":name,
            "author":author,
            "gender":gender,
            }
    #verificar se não é repetido
    if contains(name=name,author=author,age=age,gender=gender):
        raise HTTPException(status_code=404, detail=f"Livro já cadastrado.")
    try:
        if not (age >= 200 and age <= ano_atual):
            raise HTTPException(status_code=400, detail="O ano de lancamento fora de intervalo.")

    except TypeError:
        raise HTTPException(status_code=400, detail="Erro no parâmetro ano, deve ser numérico")

    for k,v in validation.items():
        if len(v) < 3:
            raise HTTPException(status_code=400, detail=f'Erro: parâmetro "{k}" muito curto')

    new_book = db.DataBase(
       host=os.getenv("HOST_NAME"), database="library", user=os.getenv("USER_NAME"), password=os.getenv("PASSWORD")
    )

    #new_book.create_table()
    new_book.add_new_book(name=name, author=author, age=age, gender=gender)
    book_format ={"name":name, "author": author, "age":age, "gender":gender}

    return  book_format

@app.put("/api/update")
async def update(name: str, author: str, age: str, gender: str, book_id: str):
    new_book = db.DataBase(
        host=os.getenv("HOST_NAME"), database="library", user=os.getenv("USER_NAME"), password=os.getenv("PASSWORD")
    )

    exists = check_(book_id)

    if exists:
        new_book.update_info(
            name=name, author=author, age=age, gender=gender, book_id=book_id
        )
        return {"message":"Update"}

    raise HTTPException(status_code=404, detail=f"Livro com ID: {book_id} não encontrado.")

@app.delete("/api/delete")
async def delete(book_id):
    book = db.DataBase(
        host=os.getenv("HOST_NAME"), database="library", user=os.getenv("USER_NAME"), password=os.getenv("PASSWORD")
    )
    book.remove_book(book_id)
    return {"message":"Book deleted."}
