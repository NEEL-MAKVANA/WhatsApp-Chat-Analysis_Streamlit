import streamlit as st
import psycopg2
from psycopg2 import Error
import pandas as pd


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


def fetch_all_users(conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return users
    except Error as e:
        st.error(f"Error fetching users: {e}")
        return []


def add_user(conn, username, password):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password),
        )
        conn.commit()
        st.success("User added successfully!")
    except Error as e:
        conn.rollback()
        st.error(f"Error adding user: {e}")


def modify_user(conn, user_id, new_username, new_password):
    try:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET username = %s, password = %s WHERE id = %s",
            (new_username, new_password, user_id),
        )
        conn.commit()
        st.success("User modified successfully!")
    except Error as e:
        conn.rollback()
        st.error(f"Error modifying user: {e}")


def delete_user(conn, user_id):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
        conn.commit()
        st.success("User deleted successfully!")
    except Error as e:
        conn.rollback()
        st.error(f"Error deleting user: {e}")


def main():
    st.title("User Management App")

    # Connect to database
    conn = connect_to_database()
    if conn is None:
        return

    # Fetch all users
    users = fetch_all_users(conn)

    # Display users in tabular format
    st.subheader("All Users")
    if len(users) == 0:
        st.write("No users found.")
    else:
        df_users = pd.DataFrame(users, columns=["ID", "Username", "Password"])
        st.dataframe(df_users)

    # Add new user
    st.subheader("Add New User")
    new_username = st.text_input("Username")
    new_password = st.text_input("Password", type="password")
    if st.button("Add User"):
        if new_username and new_password:
            add_user(conn, new_username, new_password)
        else:
            st.warning("Username and password are required.")

    # Modify user
    st.subheader("Modify User")
    modify_user_id = st.text_input("User ID to modify")
    modify_new_username = st.text_input("New Username")
    modify_new_password = st.text_input("New Password", type="password")
    if st.button("Modify User"):
        if modify_user_id and modify_new_username and modify_new_password:
            modify_user(conn, modify_user_id, modify_new_username, modify_new_password)
        else:
            st.warning("User ID, new username, and new password are required.")

    # Delete user
    st.subheader("Delete User")
    delete_user_id = st.text_input("User ID to delete")
    if st.button("Delete User"):
        if delete_user_id:
            delete_user(conn, delete_user_id)
        else:
            st.warning("User ID is required.")

    # Close database connection
    conn.close()


if __name__ == "__main__":
    main()
