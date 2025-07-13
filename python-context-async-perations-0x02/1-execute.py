#!/usr/bin/env python3

import sqlite3
import os

database_path = "/home/moment/alx-backend-python/python-decorators-0x01/users.db"

class ExecuteQuery:
    def __init__(self, query, age=25):
        self.query = query
        self.age = age
        self.connection = None

    def __enter__(self):

        try:
            print("Connected to the ALX_prodev database")
            self.connection = sqlite3.connect(database_path)
            cursor = self.connection.cursor()
            cursor.execute(self.query, (self.age,))
            return cursor    
           
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()

# This is the main program execution
if __name__ == '__main__':
    # # Context manager tha changes the current working directory to get the users db
    with ExecuteQuery("SELECT * FROM users WHERE age > ?") as query_excute:
        users = query_excute.fetchall()
        print(users)