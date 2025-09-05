#!/usr/bin/python3

"""
This script implements a generator for fetching paginated data from a
database in a memory-efficient manner.
"""
import seed


def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows


def lazy_paginate(page_size):
    """
    A generator that lazily fetches and yields user data page by page.
    This approach avoids loading the entire dataset into memory.
    """
    current_offset = 0
    while True:
        # Fetch the next page of results
        page = paginate_users(page_size, current_offset)

        if not page:  # If empty, we have reached the end of the data
            break
        yield page  # Yield the page data to the caller

        # Increment the offset for the next iteration
        current_offset += page_size
