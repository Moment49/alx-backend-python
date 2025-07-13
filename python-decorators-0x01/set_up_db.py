#!/usr/bin/env python3
import sqlite3

many_users = [(1, 'wes', 'brown', 'wesbrown@gmail.com', 32),
                (2, 'tim', 'wesly', 'timwesly@ymail.com', 24), 
                (3, 'mike', 'morgan', 'mike@morgan.com', 45),
             ]

# Create a db connection
conn = sqlite3.connect('users.db')
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY,
	        first_name TEXT NOT NULL,
	        last_name TEXT NOT NULL,
	        email TEXT NOT NULL UNIQUE,
           age INTEGER NOT NULL
            )""")

# Insert to the databae table
cursor.executemany("INSERT INTO users VALUES (?,?,?,?, ?)", many_users)
conn.commit()
conn.close()
