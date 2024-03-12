import streamlit as st
import psycopg2
from urllib.parse import urlencode
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
conn = psycopg2.connect(
    dbname="WhatsAppChatAnalyser",
    user="postgres",
    password="nk168",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()


def authenticate(username, password):
    # Execute SQL query to check user credentials
    cursor.execute(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, password),
    )
    user = cursor.fetchone()
    cursor1 = conn.cursor()
    cursor1.execute("SELECT password FROM users WHERE username = %s", (username,))
    fetch_password = cursor1.fetchone()
    if fetch_password is None:
        return False

    if pass_checker(password, fetch_password[0]):
        return True

    return user


def main():
    st.title("User Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.success("Login successful!")
            # Run user_dashboard.py in a new process
            subprocess.Popen(
                # ["streamlit", "run", "--server.port", "8505", "user_dashboard.py"]
                ["streamlit", "run", "user_dashboard.py"]
            )
        else:
            st.error("Invalid username or password")

    if st.button("Not a user then sign up here"):
        subprocess.Popen(
            # ["streamlit", "run", "--server.port", "8501", "user_signup.py"]
            ["streamlit", "run", "user_signup.py"]
        )


if __name__ == "__main__":
    main()
