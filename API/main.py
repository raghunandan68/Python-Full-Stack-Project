from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from src.db import *
app=FastAPI()
class userCreate(BaseModel):
    username:str
    email:str
    password:str
class userLogin(BaseModel):
    username:str
    password:str
class addBook(BaseModel):
    owner_id:int
    title:str
    author:str
    description:str |None=None
    status:str 
class searchBook(BaseModel):
    filter_by:str
    query:str
@app.post("/register")
def register_user(user:userCreate):
    try:
        msg=add_user(user.username,user.email,user.password)
        if "successfully" in msg.lower():
            return {"message": "User added successfully."}
        else:
            raise HTTPException(status_code=400,detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@app.post("/login") 
def user_login(user:userLogin):
    try:
        success, user_id = validate_user(user.username, user.password)
        if success:
            return {"message": "User login success.", "user_id": user_id}
        else:
            raise HTTPException(status_code=400,detail="Invalid Credentials")
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@app.post("/books/add")
def add_book(book:addBook):
    try:
        sucess,msg=add_book_in_db(book.owner_id,book.title,book.author,book.description,book.status)
        if sucess:
            return {"message": "Book added successfully.", "book_id": msg}
        else:
            raise HTTPException(status_code=400,detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
@app.post("/books/search")
def search_book(book:searchBook):
    try:
        success,res=search_book_in_db(book.query,book.filter_by)
        if success:
            return {"message": "Books found successfully.", "books": res}
        else:
            raise HTTPException(status_code=400, detail=res)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
