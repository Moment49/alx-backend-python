#!/usr/bin/env python3
import sqlite3 
import functools

# Objective: create a decorator that automatically handles opening and closing database connections

# Instructions:Complete the script below by Implementing a 
# decorator with_db_connection that opens a database connection, passes it to the function and closes it afterword

def with_db_connection(func):
    """ Decorator that opens db connection passes to the func and closes afterwards""" 

    @functools.wraps(func)
    def wrapper_db_conn(*args, **kwargs):
        database_name = 'users.db'
        connect = None
        try:
            connect = sqlite3.connect(f"{database_name}")
            # pass it to the function to establish the connection and close the connection
            result = func(connect, *args, **kwargs)
            print(f"Connected to the database `{database_name}` succesfully and passed the db connection to the function: {func.__name__}")
            return result
        except Exception as e:
            print(f"Database Error occurred: {e}")
        
        finally:
            if connect:
                connect.close()

    return wrapper_db_conn

@with_db_connection 
def get_user_by_id(conn, user_id): 
    cursor = conn.cursor() 
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
    return cursor.fetchone() 

#### Fetch user by ID with automatic connection handling 
user = get_user_by_id(user_id=1)
print(user)