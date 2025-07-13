#!/usr/bin/env python3
import time
import sqlite3 
import functools


with_db_connection = __import__('1-with_db_connection')

with_db_connection = with_db_connection.with_db_connection


#### paste your with_db_decorator here
def retry_on_failure(retries, delay):

    def decorator_retry_on_failure(func):

        @functools.wraps(func)
        def wrapper_deco_retry_on_failure(*args, **kwargs):
            # set the counts to keep track of the retries
            attempts = 0
            try:
                # This is the initial try to excute the function
                result = func(*args, **kwargs)
                # return the result of the database execution
                return result
            except sqlite3.Error as e:
                for _ in range(attempts, retries):
                    # Loop to retry the sql execution function
                    try:
                        result = func(*args, **kwargs)
                        return result
                        
                    except sqlite3.Error as e:
                        print("Retrying sql execution")
                        time.sleep(delay)
                        attempts += 1
                        if attempts == retries:
                            print(f"No of retries exhausted: {retries}")
                            break
                
        return wrapper_deco_retry_on_failure
    return decorator_retry_on_failure

    

@with_db_connection
@retry_on_failure(retries=3, delay=2)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM user")
    return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)