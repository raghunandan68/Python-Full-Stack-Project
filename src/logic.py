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
    
def request_book_via_api(requester_id, book_id):
    try:
        res = requests.post(f"{API_URL}/request-book", json={
            "requester_id": requester_id,
            "book_id": book_id
        })
        if res.status_code == 200:
            return True, res.json().get("message", "Request sent successfully.")
        else:
            return False, res.json().get("detail", "Failed to send request.")
    except Exception as e:
        return False, str(e)


def get_user_requests_via_api(user_id):
    try:
        res = requests.get(f"{API_URL}/my-requests/{user_id}")
        if res.status_code == 200:
            return True, res.json().get("requests", [])
        else:
            return False, res.json().get("detail", "Failed to fetch requests.")
    except Exception as e:
        return False, str(e)


def get_requests_for_owner_via_api(owner_id):
    try:
        res = requests.get(f"{API_URL}/owner-requests/{owner_id}")
        if res.status_code == 200:
            return True, res.json().get("requests", [])
        else:
            return False, res.json().get("detail", "Failed to fetch requests.")
    except Exception as e:
        return False, str(e)


def update_request_status_via_api(request_id, new_status):
    try:
        res = requests.put(f"{API_URL}/update-request", json={
            "request_id": request_id,
            "status": new_status
        })
        if res.status_code == 200:
            return True, res.json().get("message", "Request updated successfully.")
        else:
            return False, res.json().get("detail", "Failed to update request.")
    except Exception as e:
        return False, str(e)
    
def send_message_via_api(swap_request_id, sender_id, message_text):
    try:
        res = requests.post(f"{API_URL}/send-message", json={
            "swap_request_id": swap_request_id,
            "sender_id": sender_id,
            "message_text": message_text
        })
        if res.status_code == 200:
            return True, res.json()["data"]
        else:
            return False, res.json().get("detail", "Failed to send message.")
    except Exception as e:
        return False, str(e)


def get_messages_via_api(swap_request_id):
    try:
        res = requests.get(f"{API_URL}/get-messages/{swap_request_id}")
        if res.status_code == 200:
            return True, res.json()["messages"]
        else:
            return False, res.json().get("detail", "Failed to fetch messages.")
    except Exception as e:
        return False, str(e)
