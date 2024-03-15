import streamlit as st
import psycopg2
from psycopg2 import Error
import subprocess


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


def authenticate_admin(username, password):
    conn = connect_to_database()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM admins WHERE username = %s AND password = %s",
            (username, password),
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()
        return True if admin else False
    except Error as e:
        st.error(f"Error authenticating admin: {e}")
        return False


def main():

    st.title("Admin Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if authenticate_admin(username, password):
            st.success("Login successful!")
            # st.session_state.admin_is_logged_in = True

            subprocess.Popen(["streamlit", "run", "admin_dashboard.py"])

            # Redirect to admin dashboard or another page
            # st.write("Welcome, Admin!")
        else:
            st.error("Invalid username or password")


if __name__ == "__main__":
    main()
