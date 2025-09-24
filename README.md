## Title 
Book-Swap-Platform

## Description 
The Book Swap Platform is a full-stack web application that enables users to list books they own and are willing to swap with others in the community. This platform fosters book sharing, encouraging reading and sustainability by facilitating easy book exchanges without monetary transactions.

## Key Features

1.User Registration and Authentication:
Users can sign up, log in, and manage their profiles securely. Authentication is handled using Supabase’s built-in auth services, integrating seamlessly with the backend.

2.Book Management:
Users can add books they want to swap, including details like title, author, description, and cover image. Books can be marked as available or swapped.

3.Search and Discovery:
Users can browse or search for books available for swapping by title, author, or genre.

4.Swap Requests:
Users can send swap requests to book owners. Each request tracks its status (pending, accepted, rejected, or cancelled).

5.Real-time Chat:
Once a swap request is made, users can chat in real-time to coordinate the swap details, facilitated by the messages linked to swap requests.

## Project Structure : 
Book-Swap-Platform/
|
|--src/           #core application logic
|   |---logic.py  #Business logic and task
|   |---db.py     #For database operations
|
|--API/           #Backend API
|   |---main.py   #FastAPI and API endpoints
|
|--Frontend/      #Frontend application
|   |---app.py    #Streamlit web interface
|
|--requirements.txt  #Install python dependencies
|
|--README.md      #Project Documentation
|
|--.env           #Supabase credentials(Python Variables)


## Quick Start

## Prerequisites

-Python 3.8 or higher
-A Supabase account
-Git(Push,Cloning)

## 1.Clone or download the project

## Option 1:
git clone <git-hub repository url>

## Option 2:
Download or extract the ZIP file

## 2.Install dependencies
pip install -r requirements.txt

## 3.Setup Supabase Database
1.Create a supabase project

2.Create tasks table:
--Go to SQL Editor in Supabase Project 
--Run this SQL Command:
  "SQL Command"

3.Get your credentials

## 4.Configure environment variables
1.Create a `.env` file in the project root

2.Add your supabase credentials to `.env`
SUPABASE_URL='your supabase_url'
SUPABASE_KEY='your supabase_key'

## 5.Run the application
streamlit run Frontend/app.py
The API is available at `http://localhost:8501`

## FastAPI Backend
cd api
python main.py
The API is available at `http://localhost:8000`

## How to use

## Technologies used

**Frontend**:Streamlit(Python Web framework)
**Backend**:FastAPI(Python REST API Framework)
**Database**:Supabase(Postgre-SQL based backend-as-a-service)
**Language**:Python 3.8+

## Key Components

1.src/db.py:Database operations(Handles all crud operations with supabase)
2.src/logic.py:Business logic(Handles task and processing)

## Troubleshooting

## Common Issues

1.**Module not found error**
-Make sure you have installed dependencies `pip install -r requirements.txt`
-Check that you're running commands from the correct directory

## Future Enhancements
Ideas for extending the project:

**User Authentication**:Add user accounts and login
**Task Categories**:Organize task by category
**Data Export**:Export tasks to CSV or PDF

## Support
If you encounter any issues or have questions:
Please DM : tarunreddy4433(Instagram)