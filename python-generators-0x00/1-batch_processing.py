#!/usr/bin/env python3
from seed import connect_to_prodev
from mysql.connector import Error
import time

# Write a function stream_users_in_batches(batch_size) that fetches rows in batches
def stream_users_in_batches(batch_size):
    """Generator function that streams users from the database in batches."""
    count_rows = 0
    try:
        # Establish connection to database
        connection = connect_to_prodev()
        if connection.is_connected():
            my_cursor = connection.cursor(dictionary=True)
            # Execute the query to fetch all user data
            my_cursor.execute("SELECT * FROM user_data")
            # This loop goes through and fetches each batch of data per row count
           
            start_time = time.time()
            while True:
                batch_data = my_cursor.fetchmany(batch_size)
                # This time is set to see how the data is returned 
                
                # condition to check if rows of data exists
                if not batch_data:
                    print("No batch data returned")
                    break
                for row in batch_data:
                    # time.sleep(2)
                    yield row
                count_rows += 1
                print(f"Number of rows returned per batch: {count_rows}")
            end_time = time.time()
            print(f"Time taken for batch operation: {round(end_time - start_time, 3)}secs")
            my_cursor.close()
        connection.close()
    except Error as err:
        print(f"Error: {err}")
        return False


def batch_processing(batch_size):
    """A function that process batch data to filter users over 25 years"""
    count_rows = 0
    try:
        connection = connect_to_prodev()
        if connection.is_connected():
            mycursor = connection.cursor(dictionary=True)
            mycursor.execute("SELECT * FROM user_data")
           
            start_time = time.time()
            while True:
                data_batch = mycursor.fetchmany(batch_size)

                if not data_batch:
                    return None
                for data in data_batch:
                    # check if each user data is greater than 25 if the are yield that data
                    if data['age'] > 25:
                        yield data
                        count_rows += 1
                    print(f"Number of rows returned per batch: {count_rows}")
                end_time = time.time()
                print(f"Time taken for batch operation: {round(end_time - start_time, 3)}secs")

        connection.close()
    except Error as err:
        print(f"Error: {err}")

