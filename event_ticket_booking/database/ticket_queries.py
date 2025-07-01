import sqlite3
from event_ticket_booking.database.db_connection import DBConnection

class TicketQueries:
    def __init__(self, db_file):
        self.db_file = db_file
        self.db = DBConnection(self.db_file)
        self.connection = self.db.connect()
        self.cursor = self.connection.cursor()

    @staticmethod
    def generate_ticket_id(id, user_id, event_id):
        id_part = f"{id:02d}"
        return f"{event_id}{user_id}{id_part}"


    def add_ticket(self, user_id, event_id, price, booking_time):
        try:
            insert_query = """
                INSERT INTO tickets (user_id, event_id, price, booking_time)
                VALUES (?, ?, ?, ?);
            """

            self.cursor.execute(insert_query, (user_id, event_id, price, booking_time))
            self.connection.commit()

            id = self.cursor.lastrowid
            generated_ticket_id = self.generate_ticket_id(id, user_id, event_id)

            update_query = """
                UPDATE tickets SET ticket_id = ? WHERE id = ?
            """

            self.cursor.execute(update_query, (generated_ticket_id, id))
            self.connection.commit()

            update_seat_query = """
                UPDATE events SET total_seats = total_seats - 1 WHERE event_id = ?
            """
            self.cursor.execute(update_seat_query, (event_id,))
            self.connection.commit()

            return generated_ticket_id

        except sqlite3.Error as e:
            print(f"Error: {e}")


    def remove_ticket(self, ticket_id):
        try:
            event_id = self.get_ticket_by_id(ticket_id)[2]

            delete_query = """
                DELETE FROM tickets WHERE ticket_id = ?;
            """
            self.cursor.execute(delete_query, (ticket_id,))
            self.connection.commit()

            update_seat_query = """
                UPDATE events SET total_seats = total_seats + 1 WHERE event_id = ?
            """
            self.cursor.execute(update_seat_query, (event_id,))
            self.connection.commit()

            return True
        
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_ticket_by_id(self, ticket_id):
        try:
            select_query = """
                SELECT * FROM tickets WHERE ticket_id = ?;
            """
            self.cursor.execute(select_query, (ticket_id,))
            ticket = self.cursor.fetchone()
            return ticket if ticket else None
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_all_ticket_by_event(self, event_id):
        try:
            select_query = """
                SELECT * FROM tickets WHERE event_id = ?;
            """
            self.cursor.execute(select_query, (event_id,))
            tickets = self.cursor.fetchall()
            return tickets if tickets else None
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def get_all_ticket_by_user(self, user_id):
        try:
            select_query = """
                SELECT * FROM tickets WHERE user_id = ?;
            """
            self.cursor.execute(select_query, (user_id,))
            tickets = self.cursor.fetchall()
            return tickets if tickets else None
        except sqlite3.Error as e:
            print(f"Error: {e}")


    def close_connection(self):
        self.db.close()