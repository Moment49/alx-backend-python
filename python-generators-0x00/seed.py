#!/usr/bin/env python3
import mysql.connector as connector

def connect_db():
    connc = connector.connect(
        user='root',
        password= 'Momentum.12345',
        host = "127"
    )