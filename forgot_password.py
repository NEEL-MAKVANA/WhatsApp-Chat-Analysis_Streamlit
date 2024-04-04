import streamlit as st
import psycopg2
from passlib.context import CryptContext

# -------------------- CREATE A PASSLIB CONTEXT ----------------#
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Establish connection to PostgreSQL database
conn = psycopg2.connect(
    dbname="WhatsAppChatAnalyser",
    user="postgres",
    password="nk168",
    host="localhost",
    port="5432",
)
cursor = conn.cursor()


# Function to update password in the database
def update_password(username, new_password):
    # Hash the new password
    hashed_password = pwd_context.hash(new_password)
    # Update password in the database
    cursor.execute(
        "UPDATE users SET password = %s WHERE username = %s",
        (hashed_password, username),
    )
    conn.commit()


def main():
    st.title("Forgot Password")
    username = st.text_input("Enter your username")
    new_password = st.text_input("Enter your new password", type="password")
    confirm_password = st.text_input("Confirm your new password", type="password")

    if st.button("Reset Password"):
        if new_password == confirm_password:
            # Check if the username exists in the database
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            if user:
                # Update the password
                update_password(username, new_password)
                st.success("Password reset successfully!")
            else:
                st.error("Username does not exist")
        else:
            st.error("Passwords do not match")


if __name__ == "__main__":
    main()
