import sqlite3
import streamlit as st
DB_FILE = "user_data.db"

def save_user_to_db(username, encoding):
    """Save a new user to the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, encoding) VALUES (?, ?)", (username, encoding))
        conn.commit()
        st.success(f"User '{username}' registered successfully!")
    except sqlite3.IntegrityError:
        st.error("Username already exists. Please choose a different username.")
    conn.close()


def load_users_from_db():
    """Load all users from the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, encoding FROM users")
    rows = cursor.fetchall()
    conn.close()
    return rows
