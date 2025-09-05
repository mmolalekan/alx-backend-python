# Python Generators for Data Processing

## About the Project

This project focuses on leveraging Python generators to efficiently handle large datasets and perform memory-efficient computations. By using the `yield` keyword, the project tasks demonstrate how to implement lazy-loading and iterative data access, which is crucial for optimizing performance and resource utilization in data-driven applications.

## Learning Objectives

By completing this project, you will:

- Master Python Generators: Learn to create and use generators for iterative data processing.
- Handle Large Datasets: Implement lazy loading and batch processing to work with large volumes of data without overloading memory.
- Simulate Real-World Scenarios: Develop solutions for streaming data and on-the-fly updates.
- Optimize Performance: Use generators to perform memory-efficient aggregate calculations, such as finding the average of a large dataset.
- Apply SQL Knowledge: Integrate Python with a MySQL database to fetch and manage data dynamically.

## Requirements

To successfully complete this project, you should have:

- Proficiency in Python 3.x.
- A solid understanding of the yield keyword and generator functions.
- Familiarity with SQL and database operations (specifically MySQL).
- Basic knowledge of database schema design and data seeding.
- Experience with Git and GitHub for version control.

Project Tasks
This project is broken down into a series of tasks, each demonstrating a different application of Python generators.

0. Database Setup and Seeding

- Objective: Create a MySQL database named ALX_prodev and a user_data table.
- File: seed.py
- Details: The script sets up the database, creates a table with UUID as the primary key, and populates it with sample data from a user_data.csv file.

1. Streaming Rows One by One

- Objective: Create a generator that streams individual rows from the user_data table.
- File: 0-stream_users.py
- Details: The stream_users function uses a yield statement to fetch and return one row at a time, ensuring minimal memory usage.

2. Batch Processing

- Objective: Fetch and process data from the database in batches.
- File: 1-batch_processing.py
- Details: The stream_users_in_batches function uses a generator to fetch data in chunks, and a separate batch_processing function iterates over these chunks to filter users.

3. Lazy Paginated Data

- Objective: Simulate fetching paginated data using a generator to lazily load each page as needed.
- File: 2-lazy_paginate.py
- Details: The lazy_paginate function implements a generator that calls an external paginate_users function, fetching only one page of data at a time.

4. Memory-Efficient Aggregation

- Objective: Compute an aggregate function (average age) on a large dataset without loading it entirely into memory.
- File: 4-stream_ages.py
- Details: A generator, stream_user_ages, yields ages one by one, and a separate function uses this stream to calculate the average age.

## Project Structure

.
├── 0-main.py
├── 0-stream_users.py
├── 1-batch_processing.py
├── 1-main.py
├── 2-lazy_paginate.py
├── 2-main.py
├── 3-main.py
├── 4-stream_ages.py
├── seed.py
└── README.md

## How to Run

1. Clone the repository:

```bash
git clone alx-backend-python
cd alx-backend-python/python-generators-0x00
```

2. Run the setup script:
   This will create the database and populate the tables with sample data.

```bash
python3 0-main.py
```

3. Run individual task scripts:
   Each task has a corresponding main file to demonstrate its functionality.

```bash
# To run Task 1 (streaming users)

python3 1-main.py

# To run Task 2 (batch processing)

python3 2-main.py

# To run Task 3 (lazy pagination)

python3 3-main.py
```
