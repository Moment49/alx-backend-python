#!/usr/bin/env python3
import mysql.connector 
from mysql.connector import Error, errorcode
import os
from dotenv import load_dotenv
import pandas as pd



# Load the configuration data for the db connection
load_dotenv()

def connect_db():
    """This function is to create a db connection"""
    try:
        connection = mysql.connector.connect(
        user= os.getenv('DB_USER'),
        password= os.getenv('DB_PASSWORD'),
        host = os.getenv("DB_HOST")
        )
        print("Connection is succesfull")
        return connection

    except Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        else:
            print(err)


    
# Call the function and pass the data
connection = connect_db()
print(connection)

# Create the database
def create_database(connection):
    """This function is to create a database"""

    # create the curosor object
    my_cursor = connection.cursor()

    #Create the database
    try:
        my_cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database created successfully")
        return my_cursor, connection
    except Error as err:
        print(f"Error creating database:{err}")
        return False
  

def connect_to_prodev():
    """"This function is to connect to the ALX_prodev database"""
    try:
        database_name = "ALX_prodev"
        connection = mysql.connector.connect(
            user=os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"),
            host = os.getenv("DB_HOST"),
            database = database_name
        )
        print("Connected to the ALX_prodev database")
        return connection
    except Error as err:
        print(f"Error connecting to the database {database_name}: {err}")
    

def create_table(connection):
    """This function is to create a table"""
    try:
        my_cursor = connection.cursor()
        my_cursor.execute(
            """ CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY DEFAULT (UUID()), 
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            age DECIMAL(3, 0) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
        )
        print("Table created successfully")
    except Error as err:
        print(f"Error creating table: {err}")
        return False
    finally:
        my_cursor.close()


def insert_data(connection, data):
    """This is a function to insert data to the table""" 
    # Initialize the cursor to enable db operations
    my_cursor = connection.cursor()

    # Read the data from csv file using pandas
    df = pd.read_csv(data)

    # Convert the age to a floating datatype to match the table column "age" datatype
    df['age'] = df['age'].astype(float)

    # Loop through the dataframe with a tuple iterable which increases the efficiency
    for row in df.itertuples(index=False):
        try:
            my_cursor.execute("INSERT INTO user_data(name, email, age) VALUES (%s, %s, %s)", (row.name, row.email, row.age))
            print("Data has been inserted successfully")
            my_cursor.commit()
        except Error as err:
            print(f"This is an error: {err}")
        finally:
            # Close the cursor
            my_cursor.close()
       
            
    
    

connection = connect_db()
data = insert_data(connection, 'user_data.csv')

    

    



    