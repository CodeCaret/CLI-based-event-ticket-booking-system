from event_ticket_booking.services.db_serivce import initialize_database

from event_ticket_booking.services.user_service import UserService
from event_ticket_booking.services.event_service import EventService
from event_ticket_booking.services.booking_service import BookingService

from event_ticket_booking.utils import exceptions

import os

DB_FILE = 'booking.db'

TICKET_DIR = 'event_ticket_booking/tickets'

if not os.path.exists(TICKET_DIR):
    os.makedirs(TICKET_DIR)


def database_connection():
    global user_service, event_service, booking_service
    initialize_database(db_file=DB_FILE)
    user_service = UserService(db_file=DB_FILE)
    event_service = EventService(db_file=DB_FILE)
    booking_service = BookingService(db_file=DB_FILE, tickect_dir=TICKET_DIR)

def close_connection():
    event_service.close()
    booking_service.close()

def main_menu():
    print('\n')
    print("1. Register Manager")
    print("2. Register User")
    print("3. Login")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice


def main():
    print("Welcome to Event Booking Hub🥰")
    print("Establishing Connection With Database")
    database_connection()
    
    # try:
    #     while True:
    #         choice = main_menu()

    #         if choice == '1':
    #             pass
    #         elif choice == '2':
    #             pass
    #         elif choice == '3':
    #             pass
    #         elif choice == '4':
    #             close_connection()
    #             print("Closing Connection")
    #             print("Thank you😏! Visit Again!!!")
    #             break

    #         else:
    #             print("Invalid Choice")

    # except KeyboardInterrupt:
    #     close_connection()
    #     print("Closing Connection")
    #     print("Thank you😏! Visit Again!!!")


    # try:
    #     ticket_id = booking_service.book_ticket('USRLEO01', 'HYDCOD01', 90)
    #     print(ticket_id)
    # except exceptions.BookingError as e:
    #     print(f"Error: {e}")

    # try:
    #     if booking_service.cancel_ticket('HYDCOD01USRLEO0101'):
    #         print("Ticket Cancelled")
    # except exceptions.TicketNotFoundError as e:
    #     print(f"Error: {e}")

    # print(booking_service.ticket_list_by_event('HYDCOD01'))
    # print(booking_service.ticket_list_by_user('USRLEO01'))


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


    # try:
    #     if user_service.login_user(email="leo@gmail.com", password= 'something'):
    #         print("Logged in")
    # except exceptions.UserNotFoundError as e:
    #     print(f"Error: {e}")
    # except exceptions.IncorrectPasswordError as e:
    #     print(f"Error: {e}")


    # try:
    #     event_id = event_service.create_event('F1', 90, 'Monaco', '2025-07-12', 0)
    #     print(event_id)
    # except exceptions.BookingError as e:
    #     print(f"Error: {e}")

    # try:
    #     event = event_service.get_one_event('HYDCOD0189')
    #     print(event)
    # except exceptions.EventDoesNotExistsError as e:
    #     print(f"Error: {e}")

    # events = event_service.get_events()
    # if events:
    #     print(events)
    # else:
    #     print("OOPs No event available")


    # try:
    #     if event_service.check_availability('MONF102'):
    #         print("Seat is available")
    #     else:
    #         print("Seat is not available")
    # except exceptions.EventDoesNotExistsError as e:
    #     print(f"Error: {e}")



    # try:
    #     if event_service.delete('MONF102'):
    #         print("Event deleted")
    # except exceptions.EventDoesNotExistsError as e:
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
