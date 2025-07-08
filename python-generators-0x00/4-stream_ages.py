#!/usr/bin/env python3
from mysql.connector import Error

seed = __import__('seed')
import time


def stream_users_ages():
    """Generator function that streams users from the database and filters by age."""
    try:
        connection = seed.connect_to_prodev()
        if connection.is_connected():
            my_cursor = connection.cursor(dictionary=True)
            my_cursor.execute("SELECT * FROM user_data")
            rows = my_cursor.fetchall()

            # Loop through the data and yeild just the ages of users
            for row in rows:
                yield row['age']
            
    except Error as err:
        print(f"Error: {err}")


def aggregate_users_avg():
    """A function to get the sum of users avg age"""
    sum_ages = 0
    count = 0
    ages = stream_users_ages()
    for age in ages:
        sum_ages += age
        count += 1
    AVG_AGE = sum_ages/count
   
    return AVG_AGE

if __name__ == "__main__":
    # List of user ages returned from the data stream
    user_ages = stream_users_ages()
    for user_age in user_ages:
        print(f"Users age: {user_age}")
    
    # Print Average Age of users returned
    AVG_AGE = aggregate_users_avg()
    print(f"Average age of users: {AVG_AGE}")



