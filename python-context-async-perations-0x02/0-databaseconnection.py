#!/usr/bin/env python3
import sqlite3 
import os
from contextlib import contextmanager

DATABASE_PATH = '../python-decorators-0x01'

@contextmanager
def change_directory(destination):
    # get the current working directory
    cwd = os.getcwd()
    os.chdir(destination)
    try:
        yield os.getcwd()
    finally:
        os.chdir(cwd)


class DatabaseConnection:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
    
    def __enter__(self):
        # connect to the database
        try:
             self.connection = sqlite3.connect(self.database_name)
             cursor = self.connection.cursor()
             print(cursor)
             return cursor
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

# This is the main program execution
if __name__ == '__main__':
    # # Context manager tha changes the current working directory to get the users db
    with change_directory(DATABASE_PATH) as new_dir:
        db_path  = os.path.join(new_dir, 'users.db')
        print(db_path)
   
        with DatabaseConnection(db_path) as cursor:
            cursor.execute(" SELECT * FROM users")
            users_data = cursor.fetchall()
            print(users_data)
