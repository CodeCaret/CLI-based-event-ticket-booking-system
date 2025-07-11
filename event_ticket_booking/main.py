from event_ticket_booking.services.db_serivce import initialize_database
from event_ticket_booking.services.user_service import UserService
from event_ticket_booking.services.event_service import EventService
from event_ticket_booking.services.booking_service import BookingService

from event_ticket_booking.utils import exceptions
from event_ticket_booking.utils.animation import round_loading_animation, dot_loading_animation

from valinix import validate_password, ValidationError
from datetime import datetime

import os

CEO_PASS = 'ceo@123'

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
    user_service.close()
    event_service.close()
    booking_service.close()



def main_menu():
    print('\n')
    print("1. Register Manager")
    print("2. Register User")
    print("3. Login")
    print("4. Exit")
    choice = input("\nEnter your choice: ")
    return choice


def manager_menu():
    print('\n')
    print("1. Add Event")
    print("2. Remove Event")
    print("3. Display Events")
    print("4. Display Specific Event")
    print("5. Logout")
    choice = input("\nEnter your choice: ")
    return choice


def user_menu():
    print('\n')
    print("1. Book Ticket")
    print("2. Cancel Ticket")
    print("3. Display Events")
    print("4. Display Specific Event")
    print("5. Display Specific Ticket Information")
    print("6. Display All Ticket Information")
    print("7. Logout")
    choice = input("\nEnter your choice: ")
    return choice




def register_manager():
    ceo_pass = input("Enter CEO Password: ")
    if ceo_pass == CEO_PASS:
        name = input("Enter Your Name: ").title()
        email = input("Enter Your Email: ").lower()
        password = input("Enter Password: ")
        conf_password = input("Enter Password(again): ")
        print("\n")
        if password == conf_password:
            try:
                validate_password(password)
                manager_id = user_service.register_manager(name=name, email=email, password=password)
                print(f"Registration Successfull!")
                print(f"Your Manager ID: {manager_id}")
            except ValidationError as e:
                print(f"{e}")
            except exceptions.UserAlreadyExistsError as e:
                print(f"Error: {e}")
        else:
            print("Password Does not match. Try Again!")
    else:
        print("Incorrect Password. Try Again!")


def register_user():
    name = input("Enter Your Name: ").title()
    email = input("Enter Your Email: ").lower()
    password = input("Enter Password: ")
    conf_password = input("Enter Password(again): ")
    print("\n")
    if password == conf_password:
        try:
            validate_password(password)
            user_id = user_service.register_user(name=name, email=email, password=password)
            print(f"Registration Successfull!")
            print(f"Your User ID: {user_id}")
        except ValidationError as e:
            print(f"{e}")
        except exceptions.UserAlreadyExistsError as e:
            print(f"Error: {e}")
    else:
        print("Password Does not match. Try Again!")


def login():
    email = input("Enter Your Email: ").lower()
    password = input("Enter Password: ")
    print('\n')
    try:
        user = user_service.login_user(email=email, password=password)
        print('\n')
        print(f"Welcome {user[1]}")
        return user
    except exceptions.UserNotFoundError as e:
        print(e)
    except exceptions.IncorrectPasswordError as e:
        print(e)



def add_event():
    title = input("Enter Event Title: ").title()
    while True:
        try:
            event_price = int(input("Enter Event Price: "))
            if event_price < 0:
                print("Price should be positive value")
            else:
                break
        except ValueError:
            print("Price Should be number")

    location = input("Enter Event Location: ")

    while True:
        try:
            date_time = input("Enter Event Timings(YYYY-MM-DD HH:MM): ")
            datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            break
        except ValueError:
            print("Follow correct date time format.")

    while True:
        try:
            total_seats = int(input("Enter Total Number of  seats: "))
            if total_seats < 0:
                print("Seat Number should be positive value")
            else:
                break
        except ValueError:
            print("Seat Should be number")

    try:
        event_id = event_service.create_event(title=title, event_price=event_price, location=location, date_time=date_time, total_seats=total_seats)
        print(f"Event Added Successfully")
        print(f"Event Id: {event_id}")
    except exceptions.BookingError as e:
        print(f"Error: {e}")


def remove_event():
    try:
        event_id = input("Enter event ID: ").upper()
        event_service.delete(event_id=event_id)
        print(f"Event with ID: '{event_id}' removed successfully!")
    except exceptions.EventDoesNotExistsError as e:
        print(f"Error: {e}")


def display_events():
    events = event_service.get_events()

    if not events:
        print("OOPs! No Events scheduled as of now")
        return
    
    headers = ["EVENT ID", "EVENT TITLE", "PRICE", "LOCATION", "SHOW TIME", "AVAILABLE SEATS"]

    col_widths = [max(len(header), max(len(str(event[i])) for event in events)) for i, header in enumerate(headers)]

    col_widths = [width + 2 for width in col_widths]

    row_format = "".join([f"{{:<{col_width}}}" for col_width in col_widths])

    print("\n")
    print(row_format.format(*headers))
    print("-" * sum(col_widths))

    for event in events:
        event_id = str(event[6])
        event_title = str(event[1])
        price = f"{event[2]:.2f}"
        location = str(event[3])
        show_time = str(event[4])
        available_seats = str(event[5]) if event[5] else "Sold Out!"
        
        print(row_format.format(event_id, event_title, price, location, show_time, available_seats))



def display_specific_event():
    try:
        event_id = input("Enter event ID: ").upper()
        event = event_service.get_one_event(event_id=event_id)
        print('\n')

        headers = ["EVENT ID", "EVENT TITLE", "PRICE", "LOCATION", "SHOW TIME", "AVAILABLE SEATS"]
        col_widths = [12, 20, 8, 15, 15, 18]

        row_format = f"{{:<{col_widths[0]}}}{{:<{col_widths[1]}}}{{:<{col_widths[2]}}}{{:<{col_widths[3]}}}{{:<{col_widths[4]}}}{{:<{col_widths[5]}}}"

        print(row_format.format(*headers))
        print("-" * sum(col_widths))

        event_id = event[6]
        title = event[1]
        price = f"{event[2]:.2f}"
        location = event[3]
        show_time = event[4]
        seats = str(event[5]) if event[5] else "Sold Out!"

        print(row_format.format(event_id, title, price, location, show_time, seats))

    except exceptions.EventDoesNotExistsError as e:
        print(f"Error: {e}")


def payment(ticket_amount):
    amount = float(input("Enter the amount to do the payment: "))
    if amount == ticket_amount:
        return True
    else:
        return False


def book_ticket(user_data):
    try:
        event_id = input("Enter event ID: ").upper()
        event = event_service.get_one_event(event_id=event_id)
        if event_service.check_availability(event_id=event_id):
            print(f"Price of the '{event[1]}' event is Rs.{event[2]}")
            if payment(ticket_amount=event[2]):
                ticket_id = booking_service.book_ticket(user_id=user_data[5], event_id=event_id, price=event[2])
                ticket = booking_service.get_one_ticket(ticket_id=ticket_id)
                booking_service.generate_ticket_file(ticket_id=ticket_id, user_id=user_data[5], username=user_data[1], event_id=event_id, event_name=event[1], event_location=event[3], price=event[2], booking_time=ticket[4])
                print("Ticket Booked Successfully!🥰")
                print(f"Enjoy '{event[1]}' Show")
            else:
                print("Payment Failed!")
                print("Try Again.")
        else:
            print("Ticket Not Available")
            print("Go for another event")

    except exceptions.EventDoesNotExistsError as e:
        print(f"Error: {e}")
    except exceptions.BookingError as e:
        print(f"Error: {e}")
    except exceptions.TicketNotFoundError as e:
        print(f"Error: {e}")


def cancel_ticket():
    try:
        ticket_id = input("Enter Ticket ID: ")
        if booking_service.cancel_ticket(ticket_id=ticket_id):
            print(f"Ticket with ID: {ticket_id} Cancelled")
    except exceptions.TicketNotFoundError as e:
        print(f"Error: {e}")


def display_specific_ticket():
    try:
        ticket_id = input("Enter Ticket ID: ")
        ticket_info = booking_service.get_one_ticket_information(ticket_id=ticket_id)
        print(f"\nBelow is your Ticket Information")
        print('--------------------------------------')
        print(ticket_info)
    except exceptions.TicketNotFoundError as e:
        print(f"Error: {e}")


def display_tickets(user_id):
    tickets = booking_service.ticket_list_by_user(user_id=user_id)

    if not tickets:
        print("OOPs! No Tickets Booked")
        return

    print("\n")

    headers = ["TICKET ID", "EVENT ID", "PRICE", "BOOKING TIME"]
    col_widths = [22, 12, 8, 20]

    row_format = f"{{:<{col_widths[0]}}}{{:<{col_widths[1]}}}{{:<{col_widths[2]}}}{{:<{col_widths[3]}}}"

    print(row_format.format(*headers))
    print("-" * sum(col_widths))

    for ticket in tickets:
        ticket_id = ticket[5]
        event_id = ticket[2]
        price = f"{ticket[3]:.2f}"
        booking_time = ticket[4]
        print(row_format.format(ticket_id, event_id, price, booking_time))



def main():
    print('\n\n')
    round_loading_animation("Loading Event Booking Hub", 1)
    print("Welcome to Event Booking Hub🥰")
    dot_loading_animation("Establishing Connection", 1)
    print("Connection Established")
    database_connection()
    
    try:
        while True:
            choice = main_menu()

            if choice == '1':
                register_manager()
            elif choice == '2':
                register_user()
            elif choice == '3':
                user = login()
                if user:
                    if user_service.check_manager(email=user[2]):

                        while True:
                            manager_choice = manager_menu()
                            manager_data = user
                            
                            if manager_choice == '1':
                                add_event()
                            elif manager_choice == '2':
                                remove_event()
                            elif manager_choice == '3':
                                display_events()
                            elif manager_choice == '4':
                                display_specific_event()
                            elif manager_choice == '5':
                                print("Logged Out.")
                                print("Visit Again!")
                                break
                            else:
                                print("Invalid Choice")

                    elif user_service.check_user(email=user[2]):
                        while True:
                            user_choice = user_menu()
                            user_data = user

                            if user_choice == '1':
                                book_ticket(user_data = user_data)
                            elif user_choice == '2':
                                cancel_ticket()
                            elif user_choice == '3':
                                display_events()
                            elif user_choice == '4':
                                display_specific_event()
                            elif user_choice == '5':
                                display_specific_ticket()
                            elif user_choice == '6':
                                display_tickets(user_id=user_data[5])
                            elif user_choice == '7':
                                print("Logged Out.")
                                print("Visit Again!")
                                break
                            else:
                                print("Invalid Choice")

            elif choice == '4':
                close_connection()
                dot_loading_animation("Closing Connection", 1)
                print("Connection Closed")
                round_loading_animation("Exiting Event Booking Hub", 1)
                print("Thank you😏! Visit Again!!!")
                break

            else:
                print("Invalid Choice")

    except KeyboardInterrupt:
        print("Ctrl+c detected, Closing Gracefully!")
        close_connection()
        dot_loading_animation("Closing Connection", 1)
        print("Connection Closed")
        round_loading_animation("Exiting Event Booking Hub", 1)
        print("Thank you😏! Visit Again!!!")
