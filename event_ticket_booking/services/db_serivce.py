import sqlite3
from event_ticket_booking.database.db_connection import DBConnection

def initialize_database(db_file = 'booking.db', schema_path = 'event_ticket_booking/database/schema.sql'):

    db = DBConnection(db_file)
    connection = db.connect()
    cursor = connection.cursor()

    try:
        with open(schema_path, 'r') as file:
            script = file.read()
            cursor.executescript(script)

    except sqlite3.OperationalError as e:
        print("Database Initialization Failed")
        print(f"Operational Error: {e}")
        
    finally:
        db.close()