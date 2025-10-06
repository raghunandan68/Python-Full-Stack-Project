from fastapi import *
from pydantic import BaseModel
from src.db import *
from typing import Optional
class addBook(BaseModel):
    owner_id:int
    title:str
    author:str
    description:str |None=None
    status:str 
app = FastAPI()

class userCreate(BaseModel):
    username: str
    email: str
    password: str

class userLogin(BaseModel):
    username: str
    password: str

class searchBook(BaseModel):
    filter_by: str
    query: str

class RequestBook(BaseModel):
    requester_id: int
    book_id: int

class UpdateRequest(BaseModel):
    request_id: int
    status: str

class MessageCreate(BaseModel):
    swap_request_id: int
    sender_id: int
    message_text: str


@app.post("/register")
def register_user(user: userCreate):
    try:
        msg = add_user(user.username, user.email, user.password)
        if "successfully" in msg.lower():
            return {"message": "User added successfully."}
        else:
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def user_login(user: userLogin):
    try:
        success, user_id = validate_user(user.username, user.password)
        if success:
            return {"message": "User login success.", "user_id": user_id}
        else:
            raise HTTPException(status_code=400, detail="Invalid Credentials")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/books/add")
async def add_book(
    owner_id: int = Form(...),
    title: str = Form(...),
    author: str = Form(...),
    description: str | None = Form(None),
    status: str = Form(...),
    file: UploadFile | None = File(None)
):
    try:
        file_url = None
        if file:
            file_url = upload_book_file(owner_id, file)
        success, msg = add_book_in_db(
            owner_id,
            title,
            author,
            description,
            status,
            file_url
        )
        if success:
            return {"message": "Book added successfully.", "book_id": msg, "file_url": file_url}
        else:
            raise HTTPException(status_code=400, detail=msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/books/search")
def search_book(book: searchBook):
    try:
        success, res = search_book_in_db(book.query, book.filter_by)
        if success:
            return {"message": "Books found successfully.", "books": res}
        else:
            raise HTTPException(status_code=400, detail=res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/request-book")
def request_book(data: RequestBook):
    success, msg = request_book_in_db(data.requester_id, data.book_id)
    if success:
        return {"message": msg}
    raise HTTPException(status_code=400, detail=msg)


@app.get("/my-requests/{user_id}")
def my_requests(user_id: int):
    success, res = get_user_requests_from_db(user_id)
    if success:
        return {"requests": res}
    raise HTTPException(status_code=404, detail=res)


@app.get("/owner-requests/{owner_id}")
def owner_requests(owner_id: int):
    success, res = get_requests_for_owner_from_db(owner_id)
    if success:
        return {"requests": res}
    raise HTTPException(status_code=404, detail=res)


@app.put("/update-request")
def update_request(data: UpdateRequest):
    success, msg = update_request_status_in_db(data.request_id, data.status)
    if success:
        return {"message": msg}
    raise HTTPException(status_code=400, detail=msg)


@app.post("/send-message")
def send_message(data: MessageCreate):
    success, res = add_message_in_db(data.swap_request_id, data.sender_id, data.message_text)
    if success:
        return {"message": "Message sent successfully", "data": res}
    raise HTTPException(status_code=400, detail=res)


@app.get("/get-messages/{swap_request_id}")
def get_messages(swap_request_id: int):
    success, res = get_messages_in_db(swap_request_id)
    if success:
        return {"messages": res}
    raise HTTPException(status_code=400, detail=res)
