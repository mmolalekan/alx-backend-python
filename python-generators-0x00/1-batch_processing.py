"""
This script contains generator functions for fetching and processing
data from a MySQL database in manageable batches.
"""
import os
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()


def stream_users_in_batches(batch_size):
    """
    A generator that retrieves user records from the database in specific batch sizes.
    Each yielded item is a list of user dictionaries.
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

        current_batch = []
        for row in cursor:
            current_batch.append(row)
            if len(current_batch) == batch_size:
                yield current_batch
                current_batch = []

        # Yield any remaining rows in the final batch
        if current_batch:
            yield current_batch

    except Error as e:
        print(f"Database error: {e}")
        return
        # The generator will stop here
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'db_connection' in locals() and db_connection:
            db_connection.close()


def batch_processing(batch_size):
    """
    Processes each batch of users and prints out those whose age exceeds 25.
    """
    for user_batch in stream_users_in_batches(batch_size):
        for user in user_batch:
            if user.get("age") and user["age"] > 25:
                print(user)
