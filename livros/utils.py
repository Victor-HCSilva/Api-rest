from database import DataBase
from fastapi import FastAPI, HTTPException

"""Verifica se o livro realmente existe na base de dados"""
def check_(book_id:int) -> bool:
    book = DataBase(
        host="localhost", database="library", user="root", password="V1ct0r_Hug@"
    )
    if book.get_book(book_id):
        return True
    return

"""Retorna False se o livro não existir,
e True caso já exista"""
def contains(name:str , author:str ,gender: str,age:int ) -> bool:
    book = DataBase(
        host="localhost", database="library", user="root", password="V1ct0r_Hug@"
    )

    livros = book.list_all()

    try:
        for l in livros:
            if name == l[1] and author==l[2] and age==l[3]:
                return True
    except Exception as error:
        raise HTTPException(status_code=400, detail=f"Erro: {error}")
    return False
c = contains("c","s","s","@")
