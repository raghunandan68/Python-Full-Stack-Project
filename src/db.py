import os
from supabase import Client,create_client
from dotenv import load_dotenv
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")
sb : Client=create_client(url,key)
def add_user(user_name,user_email,password):
    payload={"username":user_name,"email":user_email,"password":password}
    res=sb.table("users").insert(payload).execute()
    if(res.data):
        return "User added successfully."
    else:
        return "Failed to add user."

def validate_user(username,password):
    res = sb.table("users")\
        .select("id","username","password")\
        .eq("username", username)\
        .eq("password", password)\
        .execute()
    if(res.data):
        user_id = res.data[0]["id"]
        return True, user_id
    else:
        return False, None

def add_book_in_db(owner_id,title,author,description,status):
    payload={"owner_id":owner_id,"title":title,"author":author,"description":description,"status":status}
    res=sb.table("books").insert(payload).execute()
    if(res.data):
        return True, res.data[0]["id"] 
    elif res.error:
        return False, f"Database error: {res.error.message}"
    else:
        return "Unable to add the book."
    
def search_book_in_db(query,filter_by:str="title"):
    try:
        if filter_by=="author":
            res = sb.table("books")\
                    .select("*")\
                    .ilike("author", f"%{query}%")\
                    .execute()
        else: 
            res = sb.table("books")\
                    .select("*")\
                    .ilike("title", f"%{query}%")\
                    .execute()
        if res.data:
            return True, res.data
        else:
            return False, "No books found."
    except Exception as e:
        return False, f"Database error: {str(e)}"