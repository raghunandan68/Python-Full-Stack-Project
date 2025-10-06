import os
from supabase import Client, create_client
from dotenv import load_dotenv
import uuid

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")
sb: Client = create_client(url, key)


def add_user(user_name, user_email, password):
    payload = {"username": user_name, "email": user_email, "password": password}
    res = sb.table("users").insert(payload).execute()
    if res.data:
        return "User added successfully."
    else:
        return "Failed to add user."


def validate_user(username, password):
    res = (
        sb.table("users")
        .select("id", "username", "password")
        .eq("username", username)
        .eq("password", password)
        .execute()
    )
    if res.data:
        user_id = res.data[0]["id"]
        return True, user_id
    else:
        return False, None


def upload_book_file(owner_id, file):
    bucket = "book_files"
    unique_name = f"{owner_id}/{uuid.uuid4()}_{file.filename}"
    try:
        file_bytes = file.file.read()
        sb.storage.from_(bucket).upload(unique_name, file_bytes, file_options={"content-type": file.content_type})
        file_url = sb.storage.from_(bucket).get_public_url(unique_name)
        if isinstance(file_url, dict) and "publicUrl" in file_url:
            return file_url["publicUrl"]
        return file_url 
    except Exception as e:
        raise Exception(f"File upload failed: {str(e)}")





def add_book_in_db(owner_id, title, author, description, status, file_url=None):
    payload = {
        "owner_id": owner_id,
        "title": title,
        "author": author,
        "description": description,
        "status": status,
        "file_url": file_url
    }
    res = sb.table("books").insert(payload).execute()
    if res.data:
        return True, res.data[0]["id"]
    elif res.error:
        return False, f"Database error: {res.error.message}"
    else:
        return False, "Unable to add the book."



def search_book_in_db(query, filter_by: str = "title"):
    try:
        if filter_by == "author":
            res = sb.table("books").select("id, title, author, status, owner_id, file_url").ilike("author", f"%{query}%").execute()
        else:
            res = sb.table("books").select("id, title, author, status, owner_id, file_url").ilike("title", f"%{query}%").execute()

        if res.data:
            books = [
                {
                    "id": b["id"],
                    "title": b["title"],
                    "author": b["author"],
                    "status": b["status"],
                    "owner_id": b["owner_id"],
                    "file_url": b.get("file_url")   
                }
                for b in res.data
            ]
            return True, res.data
        else:
            return False, "No books found."
    except Exception as e:
        return False, f"Database error: {str(e)}"
def request_book_in_db(requester_id, book_id):
    try:
        book_res = sb.table("books").select("id, owner_id, status").eq("id", book_id).execute()
        if not book_res.data:
            return False, "Book not found."

        book = book_res.data[0]
        if book["status"] != "available":
            return False, "Book is not available."
        if book["owner_id"] == requester_id:
            return False, "You cannot request your own book."
        payload = {
            "requester_id": requester_id,
            "owner_id": book["owner_id"],
            "book_id": book_id,
            "status": "pending",
        }
        res = sb.table("swap_requests").insert(payload).execute()
        if res.data:
            return True, "Book request sent successfully!"
        else:
            return False, "Failed to send request."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def get_user_requests_from_db(user_id):
    try:
        res = (
            sb.table("swap_requests")
            .select("id, status, book_id, books(title, author, file_url)")
            .eq("requester_id", user_id)
            .execute()
        )
        if res.data:
            requests = [
                {
                    "request_id": r["id"],
                    "title": r["books"]["title"],
                    "author": r["books"]["author"],
                    "status": r["status"],
                    "file_url": r["books"].get("file_url")
                }
                for r in res.data
            ]

            return True, requests
        else:
            return False, "No requests found."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def get_requests_for_owner_from_db(owner_id):
    try:
        res = (
            sb.table("swap_requests")
            .select("id, status, book_id, requester_id, users!swap_requests_requester_id_fkey(username), books(title, file_url)")
            .eq("owner_id", owner_id)
            .execute()
        )

        if res.data:
            requests = [
            {
                "request_id": r["id"],
                "book_title": r["books"]["title"],
                "requester": r["users"]["username"],
                "status": r["status"],
                "file_url": r["books"].get("file_url") 
            }
            for r in res.data
        ]


            return True, requests
        else:
            return False, "No requests for your books."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def update_request_status_in_db(request_id, new_status):
    try:
        res = sb.table("swap_requests").update({"status": new_status}).eq("id", request_id).execute()
        if res.data:
            return True, f"Request {new_status} successfully."
        else:
            return False, "Request not found or update failed."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def add_message_in_db(swap_request_id, sender_id, message_text):
    try:
        payload = {
            "swap_request_id": swap_request_id,
            "sender_id": sender_id,
            "message_text": message_text,
        }
        res = sb.table("messages").insert(payload).execute()
        if res.data:
            return True, res.data[0]
        else:
            return False, "Failed to send message."
    except Exception as e:
        return False, f"Database error: {str(e)}"


def get_messages_in_db(swap_request_id):
    try:
        res = sb.table("messages") \
            .select("id, swap_request_id, sender_id, message_text, timestamp, users(username)") \
            .eq("swap_request_id", swap_request_id) \
            .order("timestamp", desc=False) \
            .execute()

        if res.data:
            messages = [
                {
                    "id": m["id"],
                    "swap_request_id": m["swap_request_id"],
                    "sender_id": m["sender_id"],
                    "sender": m["users"]["username"] if m.get("users") else None,
                    "message_text": m["message_text"],
                    "timestamp": m["timestamp"],
                }
                for m in res.data
            ]
            return True, messages
        else:
            return True, []
    except Exception as e:
        return False, f"Database error: {str(e)}"