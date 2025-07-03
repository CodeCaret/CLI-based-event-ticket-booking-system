from event_ticket_booking.database.ticket_queries import TicketQueries

from event_ticket_booking.models.ticket import Ticket

from event_ticket_booking.utils import exceptions

from datetime import datetime
current_date_time = datetime.today().strftime("%Y-%m-%d %H:%M")

import os

class BookingService:
    def __init__(self, db_file, tickect_dir):
        self.db_file = db_file
        self.tickect_dir = tickect_dir
        self.ticket_queries = TicketQueries(self.db_file)


    def book_ticket(self, user_id, event_id, price):
        ticket = Ticket(user_id, event_id, price, current_date_time)
        ticket_id = self.ticket_queries.add_ticket(user_id=ticket.user_id, event_id=ticket.event_id, price=ticket.price, booking_time=ticket.booking_time)
        if ticket_id:
            return ticket_id
        else:
            raise exceptions.BookingError


    def generate_ticket_file(self, ticket_id, user_id, username, event_id, event_name, event_location, price, booking_time):
        ticket_file = f"{self.tickect_dir}/ticket_{ticket_id}.txt"
        with open(ticket_file, 'w') as file:
            file.write(f"Ticket ID: {ticket_id}\n")
            file.write(f"User ID: {user_id}\n")
            file.write(f"User Name: {username}\n")
            file.write(f"Event ID: {event_id}\n")
            file.write(f"Event Name: {event_name}\n")
            file.write(f"Event Location: {event_location}\n")
            file.write(f"Price: {price}\n")
            file.write(f"Booking Date & Time: {booking_time}\n")
        print(f"Ticket Generated at '{ticket_file}' path")


    def cancel_ticket(self, ticket_id):
        if self.get_one_ticket(ticket_id=ticket_id):
            if self.ticket_queries.remove_ticket(ticket_id=ticket_id):
                os.remove(f"{self.tickect_dir}/ticket_{ticket_id}.txt")
                return True


    def get_one_ticket(self, ticket_id):
        ticket = self.ticket_queries.get_ticket_by_id(ticket_id=ticket_id)
        if ticket:
            return ticket
        else:
            raise exceptions.TicketNotFoundError
        

    def ticket_list_by_event(self, event_id):
        return self.ticket_queries.get_all_ticket_by_event(event_id=event_id)


    def ticket_list_by_user(self, user_id):
        return self.ticket_queries.get_all_ticket_by_user(user_id=user_id)


    def close(self):
        self.ticket_queries.close_connection()