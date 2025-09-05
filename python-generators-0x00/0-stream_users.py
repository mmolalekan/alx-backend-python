"""
A generator function that streams rows from the user_data
table in a MySQL database one record at a time.
"""
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def stream_users():
    """
    Connects to the 'ALX_prodev' database and yields
    user records one by one. This approach is highly memory-efficient.
    """
    try:
        db_connection = mysql.connector.connect(
            database="ALX_prodev",
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST")
        )
        cursor = db_connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Iterate over the cursor, yielding each row
        for user_record in cursor:
            yield user_record

    except Error as e:
        print(f"A database error occurred: {e}")
        # The generator will stop here
    finally:
        # Ensure the cursor and connection are closed in all cases
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_connection' in locals() and db_connection:
            db_connection.close()
