#!/usr/bin/env python3

import time
import sqlite3 
import functools

with_db_connection = __import__('1-with_db_connection')

with_db_connection = with_db_connection.with_db_connection


def cache_query(func):
    query_cache = {}
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # create the hashable key to store the query
        cache_key = tuple(sorted(kwargs.items()))

        if cache_key in query_cache:
            # check if query exists and return query
            print("Returning the query from cache")
            return query_cache[cache_key]
      
        result = func(*args, **kwargs)
        query_cache[cache_key] = result
        return result
        
    return wrapper

    

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)