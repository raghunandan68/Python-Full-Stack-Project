import sys
import os
import requests
import streamlit as st
API_URL="http://localhost:8000"

def register_via_api(username,email,password):
    payload={"username":username,"email":email,"password":password}
    try:
        res=requests.post(f"{API_URL}/register",json=payload)
        if res.status_code==200:
            return True,res.json().get("message", "User registered successfully.")
        else:
            return False, res.json().get("detail", "Registration failed.")
    except Exception as e:
        return False, str(e)
    

def login_via_api(username,password):
    payload = {"username": username, "password": password}
    try:
        res=requests.post(f"{API_URL}/login",json=payload)
        if res.status_code==200:
            data=res.json()
            return True,res.json()
        else:
            return False, res.json().get("detail", "Login failed.")
    except Exception as e:
        return False, str(e)
    

def add_book_via_api(owner_id,title,author,description,status):
    payload={"owner_id":owner_id,"title":title,"author":author,"description":description,"status":status}
    try:
        res=requests.post(f"{API_URL}/books/add",json=payload)
        if res.status_code==200:
            return True,res.json().get("message","Book added successfully.")
        else:
            return False,res.json().get("detail","Unable to add the book.")
    except Exception as e:
        return False,str(e)
    
def search_book_via_api(filter_by,query):
    payload={"filter_by":filter_by,"query":query}
    try:
        res=requests.post(f"{API_URL}/books/search",json=payload)
        if res.status_code==200:
            return True,res.json()
        else:
            return False,res.json().get("detail","Unable to fetch the book.")
    except Exception as e:
        return False,str(e)