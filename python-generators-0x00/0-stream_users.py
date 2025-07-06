#!/usr/bin/env python3
seed = __import__('seed')

connection  = seed.connect_to_prodev()

def stream_users():
    # Establish connection to database
    if connection:
        my_cursor = connection.cursor()



stream_users()