#!/usr/bin/env python3
import sqlite3 
import functools

# with_db_connection = __import__('1-with_db_connection')

# with_db_connection = with_db_connection.with_db_connection

# Complete the script below by writing a decorator transactional(func) that ensures a function running a database operation 
# is wrapped inside a transaction.If the function raises an error, rollback; otherwise commit the transaction.

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


def transactional(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Handle the database transaction
        #Read, Write, Commit and Rollback
        try:
            # get the connection from the args
            conn = args[0]
            result = func(*args, **kwargs)
        
            if result > 0:
                conn.commit()
                print(f"Email address updated sucessfully:`{kwargs['new_email']}`")
            
            if result == 0:
                conn.rollback()
                raise Exception("No rows were affected. Rolling back transaction.")
            
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed and rolled back: {e}")

        return result

    return wrapper


@with_db_connection 
@transactional 
def update_user_email(conn, user_id, new_email): 
    cursor = conn.cursor() 
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id)) 
    return cursor.rowcount

#### Update user's email with automatic transaction handling 
update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')
