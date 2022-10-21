from flask import g
import sqlite3
from typing import List


from config import database_file_path, schema_file_path

def get_db_connection():
    try:
        conn = sqlite3.connect(database_file_path)
        conn.row_factory = sqlite3.Row
        if 'connection' not in g:
            g.connection = conn
    except:
        exit(f"Error connecting to database: {database_file_path}")

    return g.connection


def get_cursor():
    if 'connection' not in g:
        get_db_connection()

    return g.connection.cursor()

def init_db():
    conn = get_db_connection()
    with open(schema_file_path) as f:
        conn.executescript(f.read())

    commit()

def commit():
    try:
        get_db_connection().commit()
        return True
    except:
        print("ERROR COMMITING TO DB")
        return False
