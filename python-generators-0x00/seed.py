"""
seed.py
Setup MySQL database ALX_prodev with table user_data,
and populate from user_data.csv
"""
import os
import csv
import uuid
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


# Load environment variables
load_dotenv()


def connect_db():
    """Establishes a connection to the MySQL server without specifying a database."""
    try:
        conn = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print(f"Failed to connect to MySQL server: {e}")
    return None


def create_database(conn):
    """Creates the 'ALX_prodev' database if it doesn't already exist."""
    try:
        cur = conn.cursor()
        cur.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev;")
        conn.commit()
        print("Database 'ALX_prodev' successfully created or already exists.")
    except Error as e:
        print(f"An error occurred while creating the database: {e}")
    finally:
        if cur:
            cur.close()


def connect_to_prodev():
    """Connects directly to the 'ALX_prodev' database."""
    try:
        conn = mysql.connector.connect(
            database="ALX_prodev",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )
        if conn.is_connected():
            print("Successfully connected to the 'ALX_prodev' database.")
            return conn
    except Error as e:
        print(f"Connection to 'ALX_prodev' failed: {e}")
    return None


def create_table(conn):
    """Creates the 'user_data' table with the required schema and primary key index."""
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        conn.commit()
        print("Table 'user_data' successfully created or already exists.")
    except Error as e:
        print(f"Error creating the 'user_data' table: {e}")
    finally:
        if cur:
            cur.close()


def insert_data(conn, csv_file):
    """Creates the 'user_data' table with the required schema and primary key index."""
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id CHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX (user_id)
            );
        """)
        conn.commit()
        print("Table 'user_data' successfully created or already exists.")
    except Error as e:
        print(f"Error creating the 'user_data' table: {e}")
    finally:
        if cur:
            cur.close()


if __name__ == "__main__":
    # Main execution flow
    print("Attempting to connect to MySQL server...")
    server_conn = connect_db()

    if server_conn:
        create_database(server_conn)
        server_conn.close()
        print("Server connection closed.")

        print("\nConnecting to the 'ALX_prodev' database...")
        prodev_conn = connect_to_prodev()

        if prodev_conn:
            create_table(prodev_conn)
            insert_data(prodev_conn, "user_data.csv")
            prodev_conn.close()
            print("Database connection closed.")
        else:
            print("Failed to establish a connection to 'ALX_prodev'.")
    else:
        print("Failed to connect to the MySQL server.")
