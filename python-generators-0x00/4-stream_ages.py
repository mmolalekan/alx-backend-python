#!/usr/bin/python3

"""
This script demonstrates how to compute an aggregate function
(average age) for a large dataset using a generator to
conserve memory.
"""
import os
import seed
from dotenv import load_dotenv


load_dotenv()


def stream_user_ages():
    """
    A generator that retrieves and yields the age for each user
    from the database one by one.
    """
    db_conn = seed.connect_to_prodev()
    if not db_conn:
        return

    cursor = db_conn.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data;")

    try:
        for record in cursor:
            yield record["age"]
    finally:
        cursor.close()
        db_conn.close()


def calculate_average_age():
    """
    Computes the average age of all users by iterating over
    the stream without loading the entire dataset into memory.
    """
    total_age = 0
    user_count = 0

    # Iterate over the generator to get each age
    for age in stream_user_ages():
        total_age += age
        user_count += 1

    # Calculate the average and print the result
    if user_count > 0:
        avg_age = total_age / user_count
        print(f"Average age of users: {avg_age:.2f}")
    else:
        print("No users found to calculate the average age.")


if __name__ == "__main__":
    calculate_average_age()
