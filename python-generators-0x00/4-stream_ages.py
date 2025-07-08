#!/usr/bin/env python3

seed = __import__('seed')
import time


def stream_users_ages():
    """Generator function that streams users from the database and filters by age."""
    connection = seed.connect_to_prodev()
    connection.cursor(dictionary=True)

    if connection.is_connected():
        ...