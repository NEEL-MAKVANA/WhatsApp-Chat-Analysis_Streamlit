import streamlit as st
import psycopg2
from urllib.parse import urlencode
import subprocess

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
    return user


def main():
    st.title("Login App")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = authenticate(username, password)
        if user:
            st.success("Login successful!")
            # Run another Streamlit app in a new process
            subprocess.Popen(["streamlit", "run", "--server.port", "8505", "app.py"])
            # Optionally, you can provide a link to open the app in a new tab
            # st.markdown(
            #     f"Open [Another App](http://localhost:8502/?{urlencode({'logged_in': 'true'})}) in a new tab to continue."
            # )
        else:
            st.error("Invalid username or password")


if __name__ == "__main__":
    main()
