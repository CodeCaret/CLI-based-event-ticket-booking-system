from event_ticket_booking.services.db_serivce import initialize_database

from event_ticket_booking.services.user_service import UserService

from event_ticket_booking.utils import exceptions

# from event_ticket_booking.database.user_queries import UserQueries
# from event_ticket_booking.database.event_queries import EventQueries
# from event_ticket_booking.database.ticket_queries import TicketQueries

DB_FILE = 'booking.db'

def database_connection():
    global user_service, event, ticket
    initialize_database(db_file=DB_FILE)
    user_service = UserService(db_file=DB_FILE)

    # user = UserQueries(db_file=DB_FILE)
    # event = EventQueries(db_file=DB_FILE)
    # ticket = TicketQueries(db_file=DB_FILE)


def main():
    print("Welcom to Event Booking Hub")
    print("Establishing Connection With Database")
    database_connection()

    # try:
    #     manager_id = user_service.register_manager("Shahid", "shahid@gmail.com", "something")
    #     print(manager_id)
    # except exceptions.UserAlreadyExistsError as e:
    #     print(f"Error: {e}")

    # try:
    #     user_id = user_service.register_user("Leo", "leo@gmail.com", "something")
    #     print(user_id)
    # except exceptions.UserAlreadyExistsError as e:
    #     print(f"Error: {e}")







    # print(user.add_user('John', 'joh@gmail.com', 'Simple@123', 0))
    # print(user.get_user('joh@gmail.com'))
    # print(event.add_event('Coldplay', 'Hyderabad', '2025-06-30', 100))
    # print(event.get_event_by_id('CODCOD01'))
    # print(event.get_all_event())
    # print(event.remove_event('CODCOD01'))
    # print(ticket.add_ticket('MGRJOH03', 'HYDCOL02', 120, '2025-06-29'))
    # print(ticket.get_ticket_by_id('HYDCOL02USRJOH0401'))
    # print(ticket.get_all_ticket_by_event('HYDCOL02'))
    # print(ticket.get_all_ticket_by_user('MGRJOH03'))
    # print(ticket.remove_ticket('HYDCOL02MGRJOH0303'))
