import sqlite3
from event_ticket_booking.database.db_connection import DBConnection

class UserQueries:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DBConnection(self.db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    @staticmethod
    def generate_user_id(id, name, is_admin):
        user_prefix = "MGR" if is_admin else "USR"
        name_part = name[:3].upper()
        id_part = f"{id:02d}"
        return f"{user_prefix}{name_part}{id_part}"


    def add_user(self, name, email, password, is_admin):
        try:
            insert_query = """
                INSERT INTO users (name, email, password, is_admin)
                VALUES (?, ?, ?, ?);
            """

            self.cursor.execute(insert_query, (name, email, password, is_admin))
            self.connection.commit()

            id = self.cursor.lastrowid
            generated_user_id = self.generate_user_id(id, name, is_admin)

            update_query = """
                UPDATE users SET user_id = ? WHERE id = ?
            """

            self.cursor.execute(update_query, (generated_user_id, id))
            self.connection.commit()
            return generated_user_id

        except sqlite3.Error as e:
            print(f"Error: {e}")

    def get_user(self, email):
        try:
            select_query = """
                SELECT * FROM users WHERE email = ?;
            """
            self.cursor.execute(select_query, (email,))
            user = self.cursor.fetchone()
            return user if user else None
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def close_connection(self):
        self.db.close()