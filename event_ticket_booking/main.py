from event_ticket_booking.services.db_serivce import initialize_database

DB_FILE = 'booking.db'

def database_connection():
    initialize_database(db_file=DB_FILE)


def main():
    print("Welcom to Event Booking Hub")
    print("Establishing Connection With Database")
    database_connection()
    
