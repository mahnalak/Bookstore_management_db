# Bookstore Management System

## Overview

The Bookstore Management System is a web-based application that simplifies bookstore operations, making it easier to manage book records, search for books, and ensure a seamless user experience. This guide will walk you through the setup, features, and usage of the application.

---

## Features

- Add, update, and delete book records effortlessly.
- Search functionality to quickly find books.
- User session management with Flask-Session for secure interactions.
- Responsive design for usability across all devices.

---

## Prerequisites

Before running the application, ensure you have the following installed:

- Python 3.x
- Virtualenv (optional but recommended)
- Flask and other dependencies (listed in `requirements.txt`)

---

## Setup Instructions

## 1. Clone or Download the Repository
Download the project files and navigate to the project directory:

```bash
cd bookstore_managemnet_db
```
## 2. Create and Activate a Virtual Environment (Optional but Recommended)
```
python3 -m venv venv
source venv/bin/activate   # For Linux/MacOS
venv\\Scripts\\activate    # For Windows
```
## 3. Install Dependencies
Install the required Python packages from requirements.txt:
```
pip install -r requirements.txt
```
## 4. Run the Application
Start the application using the following command:
```
python app.py
```
The application will run on http://127.0.0.1:5000 by default.

---

### Usage Guide
1. Home Page
Upon accessing the application, you'll see the home page. Use the navigation menu to explore the features.

2. Manage Book Records
Add Books: Use the "Add Book" option to enter book details.
Update Books: Click on a book and choose betweeen "Avalable" and "Rented" to modify its information.
Delete Books: Select a book and click "Delete" to remove it.

3. Search for Books
Utilize the search bar to find books quickly by title or author.

4. Session Management
User sessions ensure secure interactions. Log in or manage your session as prompted.

---

## Folder Structure
- app.py: Main application file.
- routes.py: Defines the backend logic and routes.
- templates/: Contains HTML templates for the front-end.
- static/: Holds CSS, JavaScript, and image files.
- requirements.txt: Lists all Python dependencies.
- flask_session/: Stores session data (if enabled).
---
# Group Members:
Hemangi Mahant,
Lakshita Mahna,
Tavishi Sharma,
Tushmi Sharma

