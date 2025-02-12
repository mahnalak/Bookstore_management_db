# routes.py

from flask import Flask, redirect, url_for, session, jsonify, request, render_template
from authlib.integrations.flask_client import OAuth
from flask_session import Session
from flask_cors import CORS
import psycopg2
import os

# Flask app setup
app = Flask(__name__)
app.secret_key = 'YOUR_SECRET_KEY'  # Replace with your secret key

# Session configuration
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

# CORS configuration
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}}, supports_credentials=True)

# Auth0 configuration
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id='thKluWWYvWZ2TRmh602bOVp4uG2zRciD',        # Replace with your Auth0 client ID
    client_secret='eBd7iXgHvuBZdQ1h-mwqtzKS_aXxA4POrHNcAg8X2gZkJ-hk0QQZoK07jhQ-574K',  # Replace with your Auth0 client secret
    client_kwargs={
        'scope': 'openid profile email',
    },
    server_metadata_url=f'https://dev-3ekxwc0652tdovyr.us.auth0.com/.well-known/openid-configuration',  # Replace with your Auth0 domain
)

# Function to establish database connection
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="bookstore",
        user="hemangimahant",       # Replace with your PostgreSQL username
        password="Henny81589"    # Replace with your PostgreSQL password
    )
    return conn

# Root route
@app.route("/")
def home():
    return render_template('index.html')

# Auth0 login
@app.route("/login")
def login():
    return auth0.authorize_redirect(redirect_uri="http://127.0.0.1:5000/callback")

# Auth0 callback
@app.route("/callback")
def callback():
    try:
        token = auth0.authorize_access_token()
        session['user'] = token['userinfo']
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Callback Error: {e}")
        return jsonify({"error": "Authentication failed"}), 401

# Auth0 logout
@app.route("/logout")
def logout():
    session.clear()
    logout_url = (
        f"https://dev-3ekxwc0652tdovyr.us.auth0.com/v2/logout"
        f"?client_id=thKluWWYvWZ2TRmh602bOVp4uG2zRciD"
        f"&returnTo=http://127.0.0.1:5000/"
    )
    return redirect(logout_url)

# Session info (for debugging purposes)
@app.route('/session')
def session_info():
    return jsonify(dict(session))

# Helper function to check if user is logged in
def is_logged_in():
    return 'user' in session

# Route to fetch books or filter by availability
@app.route("/books", methods=["GET", "POST"])
def books():
    if request.method == "GET":
        availability = request.args.get("availability")
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            if availability:
                cursor.execute("SELECT * FROM books WHERE b_availability = %s;", (availability,))
            else:
                cursor.execute("SELECT * FROM books;")
            books = cursor.fetchall()
            conn.close()
            return jsonify([{
                "id": row[0],
                "title": row[1],
                "author": row[2],
                "genre": row[3],
                "availability": row[4]
            } for row in books])
        except Exception as e:
            conn.close()
            print(f"Error fetching books: {e}")
            return jsonify({"error": str(e)}), 500
    elif request.method == "POST":
        if not is_logged_in():
            return jsonify({"error": "Unauthorized"}), 401
        try:
            data = request.get_json()
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO books (b_title, b_author, b_genre, b_availability) VALUES (%s, %s, %s, %s)",
                (data["title"], data["author"], data["genre"], data["availability"])
            )
            conn.commit()
            conn.close()
            return jsonify({"message": "Book added successfully!"}), 201
        except Exception as e:
            conn.close()
            print(f"Error adding book: {e}")
            return jsonify({"error": str(e)}), 500

# Route to delete or update a book (protected)
@app.route("/books/<int:book_id>", methods=["DELETE", "PUT"])
def modify_book(book_id):
    if not is_logged_in():
        return jsonify({"error": "Unauthorized"}), 401
    if request.method == "DELETE":
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM books WHERE b_id = %s RETURNING b_id;", (book_id,))
            deleted_id = cursor.fetchone()
            if deleted_id:
                cursor.execute("SELECT setval(pg_get_serial_sequence('books', 'b_id'), MAX(b_id)) FROM books;")
                conn.commit()
            conn.close()
            return jsonify({"message": f"Book with ID {book_id} deleted successfully!"})
        except Exception as e:
            conn.close()
            print(f"Error deleting book: {e}")
            return jsonify({"error": str(e)}), 500
    elif request.method == "PUT":
        try:
            data = request.get_json()
            availability = data.get("availability")
            if not availability:
                return jsonify({"error": "Availability status is required"}), 400
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE books SET b_availability = %s WHERE b_id = %s;",
                (availability, book_id)
            )
            conn.commit()
            conn.close()
            return jsonify({"message": f"Book with ID {book_id} updated successfully!"})
        except Exception as e:
            conn.close()
            print(f"Error updating book: {e}")
            return jsonify({"error": str(e)}), 500

# Route to search books
@app.route("/books/search")
def search_books():
    query = request.args.get("query")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        search_query = f"%{query}%"
        cursor.execute(
            "SELECT * FROM books WHERE b_title ILIKE %s OR b_author ILIKE %s OR b_genre ILIKE %s;",
            (search_query, search_query, search_query)
        )
        books = cursor.fetchall()
        conn.close()
        return jsonify([{
            "id": row[0],
            "title": row[1],
            "author": row[2],
            "genre": row[3],
            "availability": row[4]
        } for row in books])
    except Exception as e:
        conn.close()
        print(f"Error searching books: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
