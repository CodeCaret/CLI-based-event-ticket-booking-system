import sqlite3
from sqlite3 import Error

class DBConnection:

    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        try:
            self.connection = sqlite3.connect(self.db_file)
            self.connection.execute("PRAGMA foreign_keys = ON;")
        except Error as e:
            print("Database Error: ",e)
        return self.connection
    
    def close(self):
        if self.connection:
            self.connection.close()