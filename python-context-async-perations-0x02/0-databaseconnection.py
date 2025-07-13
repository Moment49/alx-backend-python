#!/usr/bin/env python3
import sqlite3 
import os
from contextlib import contextmanager

DATABASE_PATH = '../python-decorators-0x01'

print(os.getcwd())
os.chdir(DATABASE_PATH)
print(os.getcwd())

@contextmanager
def change_directory(destination):
    # get the current working directory
    cwd = os.getcwd()
    os.chdir(destination)
    try:
        yield os.getcwd()
    finally:
        cwd


class DatabaseConnection:
    def __init__(self, database_name):
        self.database_name = database_name
        self.connection = None
    
    def __enter__(self):
        # connect to the database
        try:
             self.connection = sqlite3.connect(self.database_name)
             self.cursor = self.connection.cursor()
             return self.cursor
        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
        return self.fileobj
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

# This is the main program execution
if __name__ == '__main__':
    # # Context manager tha changes the current working directory to get the users db
    with change_directory(DATABASE_PATH) as new_dir:
        db_path  = os.path.join(new_dir, 'users.db')
   
        with DatabaseConnection(db_path) as connect_cursor:
            connect_cursor.execute(" SELECT * FROM users")
            users_data = connect_cursor.fetchall()
            print(users_data)
