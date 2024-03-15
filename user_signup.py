import streamlit as st
import psycopg2
from psycopg2 import Error
import subprocess
from passlib.context import CryptContext

# -------------------- CREATE A PASSLIB CONTEXT ----------------#
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------- CHECK WHETHER THE HASH PASSWORD AND USER ENTERED PASSWORD IS SAME OR NOT? -------------#
def pass_checker(user_pass, hash_pass):
    if pwd_context.verify(user_pass, hash_pass):
        return True
    else:
        return False


# Establish connection to PostgreSQL database
def connect_to_database():
    try:
        conn = psycopg2.connect(
            dbname="WhatsAppChatAnalyser",
            user="postgres",
            password="nk168",
            host="localhost",
            port="5432",
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


# Function to check if username already exists in the database
def check_username_exist(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        return True if user else False
    except Error as e:
        st.error(f"Error checking username existence: {e}")
        return False


# Function to add a new user to the database
def add_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        conn.commit()
        cursor.close()
        st.success("User registered successfully!")
        return True
    except Error as e:
        conn.rollback()
        st.error(f"Error adding user: {e}")
        return False


def main():
    st.title("User Signup")

    # Connect to database
    conn = connect_to_database()
    if conn is None:
        return

    # User signup form
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    hash_password = pwd_context.hash(password)

    # Sign up button
    if st.button("Sign Up"):
        if not username or not password:
            st.warning("Username and password are required.")
        elif check_username_exist(conn, username):
            st.warning("Username already exists. Please choose a different username.")
        else:
            if add_user(conn, username, hash_password):

                # Clear form fields on successful signup
                subprocess.Popen(
                    # ["streamlit", "run", "--server.port", "8506", "user_dashboard.py"]
                    ["streamlit", "run", "user_dashboard.py"]
                )

    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()
