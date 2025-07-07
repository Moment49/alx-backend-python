#!/usr/bin/env python3

from mysql.connector import Error
from seed import connect_to_prodev

def stream_users():
    """"Generator function that streams users from the database."""
    try:
        # Establish connection to database
        connection  = connect_to_prodev()
        if connection.is_connected():
            my_cursor = connection.cursor(dictionary=True)
            # Execute the query to fetch all user data
            my_cursor.execute("SELECT * FROM user_data")
            # Fetch rows one by one
            result = my_cursor.fetchall()
            for row in result:
                yield row
            else:
                raise Error("Failed to connect to the database")
        
    except Error as err:
        print(f"Error: {err}")

                



