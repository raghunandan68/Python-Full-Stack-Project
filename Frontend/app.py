import sys
import os
import requests
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.db import *
from src.logic import *
API_URL = "http://localhost:8000"
st.set_page_config(page_title="📚 Book-Share Platform", layout="centered")
st.markdown(
    """
    <style>
        .main-title {
            font-size: 2.2em;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 0.3em;
        }
        .sub-title {
            font-size: 1.2em;
            color: #555;
            text-align: center;
            margin-bottom: 1.5em;
        }
        .card {
            padding: 1.5em;
            border-radius: 12px;
            background-color: #f9f9f9;
            box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 1em;
        }
        .stButton>button {
            border-radius: 8px;
            font-size: 1em;
            padding: 0.5em 1.2em;
        }
    </style>
    """,
    unsafe_allow_html=True
)


def show_home():
    st.markdown('<div class="main-title">📖 Welcome to Book-Share Platform</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-title">A community-driven space to share, discover, and swap books sustainably</div>',
        unsafe_allow_html=True
    )
    st.markdown("### 🌟 Why Join?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(
            """
            - ✅ Share books you no longer need  
            - 🔍 Discover hidden gems  
            - ♻️ Promote sustainability  
            """
        )
    with col2:
        st.markdown(
            """
            - 🤝 Connect with fellow readers  
            - 💬 Chat (coming soon!)  
            - 🚀 Build your reading community  
            """
        )
    st.markdown("---")
    st.write("### Choose an option to continue:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔑 Login", use_container_width=True):
            st.session_state['page'] = 'login'
    with col2:
        if st.button("📝 Register", use_container_width=True):
            st.session_state['page'] = 'register'


def show_register():
    st.markdown('<div class="main-title">📝 Create Your Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Join our community and start sharing books today!</div>', unsafe_allow_html=True)
    with st.form("user_reg_form"):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            name = st.text_input("👤 Username")
            email = st.text_input("📧 Email")
            password = st.text_input("🔒 Password", type="password")
            st.markdown('</div>', unsafe_allow_html=True)
            submit_btn = st.form_submit_button("✨ Register Now")
            if submit_btn:
                if name.strip() == "" or email.strip() == "" or password.strip() == "":
                    st.error("⚠️ Please fill all the fields.")
                else:
                    success, res = register_via_api(name, email, password)
                    if success:
                        st.success("✅ " + res)
                    else:
                        st.error("❌ " + res)

    if st.button("⬅️ Back to Home"):
        st.session_state['page'] = 'home'


def show_login():
    st.markdown('<div class="main-title">🔑 Login to Your Account</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Welcome back! Let’s continue your book journey.</div>', unsafe_allow_html=True)

    with st.form("user_login_form"):
        with st.container():
            st.markdown('<div class="card">', unsafe_allow_html=True)
            name = st.text_input("👤 Username")
            password = st.text_input("🔒 Password", type="password")
            st.markdown('</div>', unsafe_allow_html=True)

            submit_btn = st.form_submit_button("🚀 Login")
            if submit_btn:
                if name.strip() == "" or password.strip() == "":
                    st.error("⚠️ Please fill all the fields.")
                else:
                    success, res = login_via_api(name, password)
                    if success:
                        st.session_state['username'] = name
                        st.session_state['user_id'] = res.get("user_id")
                        st.session_state['page'] = 'dashboard'
                        st.rerun()
                    else:
                        st.error("❌ " + res)

    if st.button("⬅️ Back to Home"):
        st.session_state['page'] = 'home'


def show_dashboard():
    uname = st.session_state.get('username', 'User')
    st.markdown(f'<div class="main-title">📚 Welcome, {uname} 👋</div>', unsafe_allow_html=True)

    st.info(
        """
        Here’s what you can do on your dashboard:
        - ➕ Add new books to share
        - 🔍 Search books from others
        - 📬 Manage requests
        - 💬 Chat with readers (coming soon!)
        """
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("➕ Add Book", use_container_width=True):
            st.session_state['page'] = 'add_book'
            st.rerun()
    with col2:
        if st.button("🔍 Search Books", use_container_width=True):
            st.session_state['page'] = 'search_books'
            st.rerun()
    with col3:
        if st.button("📬 Request Books", use_container_width=True):
            st.session_state['page'] = 'request_book'
            st.rerun()
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.clear()
            st.session_state['page'] = 'home'
            st.rerun()


def show_add_book():
    st.markdown('<div class="main-title">➕ Add a New Book</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Share your book and make it available for others</div>', unsafe_allow_html=True)

    with st.form("add_book_form"):
        title = st.text_input("📖 Book Title")
        author = st.text_input("✍️ Author")
        description = st.text_area("📝 Description")
        status = st.selectbox("📌 Status", ["available", "swapped"])
        submit_btn = st.form_submit_button("📤 Add Book")
        owner_id = st.session_state.get("user_id")
        if submit_btn:
            if title.strip() == "" or author.strip() == "":
                st.error("⚠️ Please enter title and author")
            else:
                success, res = add_book_via_api(owner_id, title, author, description, status)
                if success:
                    st.success("✅ " + res)
                else:
                    st.error("❌ " + res)

    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = 'dashboard'


def show_search_books():
    st.markdown('<div class="main-title">🔍 Search Books</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">Find books by title or author</div>', unsafe_allow_html=True)
    with st.form("search_book_form"):
        filter_by = st.selectbox("Filter by:", ["Title", "Author"])
        query = st.text_input("🔎 Enter keyword")
        submit_btn = st.form_submit_button("Search")
        if submit_btn:
            if query.strip() == "":
                st.error("⚠️ Please enter a search keyword.")
            else:
                success, res = search_book_via_api(filter_by.lower(), query)
                if success:
                    st.success(res.get("message"))
                    books = res.get("books", [])
                    if books:
                        st.markdown("### 📚 Search Results")
                        cols = st.columns(3) 
                        for i, book in enumerate(books):
                            with cols[i % 3]:
                                st.markdown(
                                    f"""
                                    <div class="card">
                                        <h4>📖 {book['title']}</h4>
                                        <p><b>Author:</b> {book['author']}</p>
                                        <p><b>Status:</b> <span style="color:{'green' if book['status']=='available' else 'red'};">{book['status'].capitalize()}</span></p>
                                        <p style="font-size: 0.9em; color: #555;">{book.get('description', 'No description available')}</p>
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )
                    else:
                        st.info("No books found for your search.")
                else:
                    st.error("❌ " + res)

    if st.button("⬅️ Back to Dashboard"):
        st.session_state['page'] = 'dashboard'


def show_request_book():
    st.title("📚 Book Swap Requests")
    user_id = st.session_state.get("user_id")
    if not user_id:
        st.error("You must be logged in to request books.")
        return
    tab1, tab2, tab3 = st.tabs(
        ["🔍 Browse & Request", "📤 My Requests", "📥 Requests for My Books"]
    )
    with tab1:
        st.subheader("Find Books to Request")
        filter_by = st.selectbox("Search by:", ["Title", "Author"], key="browse_filter")
        query = st.text_input("Enter keyword:", key="browse_query")

        if st.button("Search", key="search_requests"):
            if query.strip() == "":
                st.error("Please enter a keyword.")
            else:
                success, res = search_book_via_api(filter_by.lower(), query)
                if success and res.get("books"):
                    st.session_state["browse_results"] = res["books"]
                else:
                    st.session_state["browse_results"] = []

        if "browse_results" in st.session_state:
            books = st.session_state["browse_results"]
            if not books:
                st.info("No books found.")
            else:
                cols = st.columns(2)
                for i, book in enumerate(books):
                    if book["status"] != "available" or book["owner_id"] == user_id:
                        continue
                    with cols[i % 2]:
                        st.markdown(
                            f"""
                            <div style="padding:15px; border:1px solid #ccc; border-radius:10px; margin-bottom:15px;">
                                <h4>{book['title']}</h4>
                                <p><b>Author:</b> {book['author']}</p>
                                <p><b>Status:</b> {book['status']}</p>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                        if st.button(f"Request '{book['title']}'", key=f"req_{book['id']}"):
                            success_req, msg = request_book_via_api(user_id, book["id"])
                            if success_req:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
    with tab2:
        st.subheader("📤 My Requests")
        success, res = get_user_requests_via_api(user_id)
        if success:
            for r in res:
                st.markdown(
                    f"**{r['title']}** by *{r['author']}* — Status: **{r['status']}**"
                )
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("💬 Chat", key=f"chat_myreq_{r['request_id']}"):
                        st.session_state["page"] = "chat"
                        st.session_state["swap_request_id"] = r["request_id"]
                        st.session_state["chat_from"] = "request_book"
                        st.rerun()
                with col2:
                    if r["status"] == "pending":
                        if st.button("❌ Cancel Request", key=f"cancel_{r['request_id']}"):
                            success_upd, msg = update_request_status_via_api(
                                r["request_id"], "cancelled"
                            )
                            if success_upd:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)
        else:
            st.info(res)
    with tab3:
        st.subheader("📥 Requests for My Books")
        success, res = get_requests_for_owner_via_api(user_id)
        if success:
            for r in res:
                st.markdown(
                    f"**{r['book_title']}** requested by *{r['requester']}* — Status: **{r['status']}**"
                )
                col1, col2, col3 = st.columns(3)
                with col1:
                    if st.button("💬 Chat", key=f"chat_ownerreq_{r['request_id']}"):
                        st.session_state["page"] = "chat"
                        st.session_state["swap_request_id"] = r["request_id"]
                        st.session_state["chat_from"] = "request_book"
                        st.rerun()
                if r["status"] == "pending":
                    with col2:
                        if st.button("✅ Accept", key=f"accept_{r['request_id']}"):
                            success_upd, msg = update_request_status_via_api(
                                r["request_id"], "accepted"
                            )
                            if success_upd:
                                st.success(msg)
                                st.rerun()
                            else:
                                st.error(msg)

                    with col3:
                        if st.button("❌ Reject", key=f"reject_{r['request_id']}"):
                            success_upd, msg = update_request_status_via_api(
                                r["request_id"], "rejected"
                            )
                            if success_upd:
                                st.warning(msg)
                                st.rerun()
                            else:
                                st.error(msg)
        else:
            st.info(res)
    if st.button("⬅️ Back to Dashboard"):
        st.session_state["page"] = "dashboard"
        st.rerun()


def show_chat(swap_request_id: int):
    st.title("📨 Chat Window")
    if "chat_from" in st.session_state:
        if st.button("⬅ Back"):
            st.session_state["page"] = st.session_state["chat_from"]
            st.rerun()
    success, messages = get_messages_via_api(swap_request_id)
    if not success:
        st.error(messages)
        return
    st.subheader("Conversation")
    for msg in messages:
        sender = "You" if msg["sender_id"] == st.session_state.get("user_id") else f"User {msg['sender_id']}"
        st.markdown(f"**{sender}:** {msg['message_text']}  \n ⏰ {msg['timestamp']}")
    with st.form("chat_form", clear_on_submit=True):
        new_message = st.text_input("Type your message...")
        send_btn = st.form_submit_button("Send")
        if send_btn and new_message.strip():
            send_message_via_api(swap_request_id, st.session_state["user_id"], new_message.strip())
            st.rerun()



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
elif st.session_state['page'] == 'add_book':
    show_add_book()
elif st.session_state['page'] == 'search_books':
    show_search_books()
elif st.session_state['page'] == 'request_book':
    show_request_book()
elif st.session_state["page"] == "chat":
    swap_request_id = st.session_state.get("swap_request_id")
    if swap_request_id:
        show_chat(swap_request_id)
    else:
        st.error("No request selected for chat.")
