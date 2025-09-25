import sys
import os
import requests
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db import *
from src.logic import *
API_URL="http://localhost:8000"
st.set_page_config(page_title="Book-Share-Platform",layout="centered")


def show_home():
    st.title("Book-Share-Platform")
    st.write("""
        **Welcome to the Book Share Platform — a community-driven app where you can**:
        - Share books you own and want to swap
        - Discover new books from others
        - Connect and chat with fellow readers
        - Promote sustainability by reusing and exchanging books without money
        
        Whether you want to share your old novels or find new favorites, this platform makes it easy and fun!
        """)
    st.write("Please Choose an option : ")
    col1,col2=st.columns(2)
    with col1:
        if st.button("Login"):
            st.session_state['page']='login'
    with col2:
        if st.button("Register"):
            st.session_state['page']='register'
    

def show_register():
    st.title("Book-Share-Platform-Register")
    st.subheader("User Registration")
    with st.form("user_reg_form"):
        name=st.text_input("Enter user name : ")
        email=st.text_input("Enter user email : ")
        password=st.text_input("Enter password : ",type="password")
        submit_btn=st.form_submit_button("Register")
        if submit_btn:
            if name.strip()=="" or email.strip()=="" or password.strip()=="":
                st.error("Please fill all the fields.")
            else:
                success,res=register_via_api(name,email,password)
                if success:
                    st.success(res)
                else:
                    st.error(res)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'


def show_login():
    st.title("Book-Share-Platform-Login")
    st.subheader("User Login")
    with st.form("user_login_form"):
        name=st.text_input("Enter username : ")
        password=st.text_input("Enter password : ",type="password")
        submit_btn=st.form_submit_button("Login")
        if submit_btn:
            if name.strip()=="" or password.strip()=="":
                st.error("Please fill all the fields.")
            else:
                success,res=login_via_api(name,password)
                if success:
                    st.session_state['username']=name
                    st.session_state['user_id']=res.get("user_id")
                    st.session_state['page']='dashboard'
                    st.rerun()
                else:
                    st.error(res)
    if st.button("Back to Home"):
        st.session_state['page'] = 'home'

def show_dashboard():
    st.title("Book-Share Dashboard")
    uname=st.session_state.get('username','User')
    st.success(f"**Welcome {uname}👋!**")
    st.write("""
    This is your dashboard where you can:
    - View your listed books
    - Manage swap requests
    - Add new books to swap
    - Chat with other users (coming soon!)
    """)
    st.write("Please Choose an option : ")
    c1,c2,c3,c4=st.columns(4)
    with c1:
        if st.button("Add Book"):
            st.session_state['page']='add_book'
            st.rerun()
    with c2:
        if st.button("Search Books"):
            st.session_state['page']='search_books'
            st.rerun()
    with c3:
        if st.button("Request Books"):
            st.session_state['page']='request_book'
            st.rerun()
    with c4:
        if st.button("Logout"):
            st.session_state.clear()
            st.session_state['page'] = 'home'
            st.rerun()



def show_add_book():
    st.title("Book-Share-Platform")
    st.subheader("Add a Book")
    with st.form("add_book_form"):
        title=st.text_input("Enter book title : ")
        author=st.text_input("Enter book author : ")
        description=st.text_input("Enter book description : ")
        status = st.selectbox("Enter book status:", ["available", "swapped"])
        submit_btn=st.form_submit_button("Add Book")
        owner_id = st.session_state.get("user_id")
        if submit_btn:
            if title.strip()=="" or author.strip()=="":
                st.error("Please enter title and author")
            else:
                success,res=add_book_via_api(owner_id,title,author,description,status)
                if success:
                    st.success(res)
                else:
                    st.error(res)
    if st.button("Back to Home"):
        st.session_state['page'] = 'dashboard'

def show_search_books():
    st.title("Book-Share-Platform")
    st.subheader("Search a Book")
    with st.form("search_book_form"):
        filter_by=st.selectbox("Search By : ",["Title","Author"])
        query = st.text_input("Enter search keyword:")
        submit_btn=st.form_submit_button("Search Book")
        if submit_btn:
            if query.strip()=="":
                st.error("Please enter a search keyword.")
            else:
                success,res=search_book_via_api(filter_by.lower(),query)
                if success:
                    st.success(res.get("message"))
                    for book in res["books"]:
                        st.write(f"**{book['title']}** by {book['author']} — {book['status']}")
                else:
                    st.error(res)
    if st.button("Back to Home"):
        st.session_state['page'] = 'dashboard'


if 'page' not in st.session_state:
    st.session_state['page'] = 'home'
if st.session_state['page'] == 'home':
    show_home()
elif st.session_state['page'] == 'register':
    show_register()
elif st.session_state['page'] == 'login':
    show_login()
elif st.session_state['page'] == 'dashboard':
    show_dashboard()
elif st.session_state['page']=='add_book':
    show_add_book()
elif st.session_state['page']=='search_books':
    show_search_books()
elif st.session_state['page']=='request_book':
    show_request_book()