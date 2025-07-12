#!/usr/bin/env python3
import sqlite3
import functools


log_file = 'log_queries.txt'

#### decorator to lof SQL queries
def log_queries(func):
    """This is a decorator function to log queries to a file"""
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        print(kwargs)
        # Open the file and log the query been executed before excuting it
        log_query = kwargs['query']
        # Write to the file
        with open(log_file, 'a') as file_obj:
            file_obj.write(f"{log_query}\n")
        print(f"The function name `{func.__name__}` executed the log query: {log_query}")
        # Excutes the query and returns the result
        result = func(*args, **kwargs)
        return result
    return wrapper_log_queries


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")