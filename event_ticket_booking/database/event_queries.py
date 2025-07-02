import sqlite3
from event_ticket_booking.database.db_connection import DBConnection

class EventQueries:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DBConnection(self.db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    @staticmethod
    def generate_event_id(id, title, location):
        location_prefix = location[:3].upper()
        title_part = title[:3].upper()
        id_part = f"{id:02d}"
        return f"{location_prefix}{title_part}{id_part}"


    def add_event(self, title, event_price, location, date_time, total_seats):
        try:
            insert_query = """
                INSERT INTO events (title, event_price, location, date_time, total_seats)
                VALUES (?, ?, ?, ?, ?);
            """

            self.cursor.execute(insert_query, (title, event_price, location, date_time, total_seats))
            self.connection.commit()

            id = self.cursor.lastrowid
            generated_event_id = self.generate_event_id(id, title, location)

            update_query = """
                UPDATE events SET event_id = ? WHERE id = ?
            """

            self.cursor.execute(update_query, (generated_event_id, id))
            self.connection.commit()
            return generated_event_id

        except sqlite3.Error as e:
            print(f"Error: {e}")


    def remove_event(self, event_id):
        try:
            delete_query = """
                DELETE FROM events WHERE event_id = ?;
            """
            self.cursor.execute(delete_query, (event_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_event_by_id(self, event_id):
        try:
            select_query = """
                SELECT * FROM events WHERE event_id = ?;
            """
            self.cursor.execute(select_query, (event_id,))
            event = self.cursor.fetchone()
            return event if event else None
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_all_event(self):
        try:
            select_query = """
                SELECT * FROM events;
            """
            self.cursor.execute(select_query)
            events = self.cursor.fetchall()
            return events if events else None
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def close_connection(self):
        self.db.close()