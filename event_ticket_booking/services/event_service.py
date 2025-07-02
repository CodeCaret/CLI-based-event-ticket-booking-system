from event_ticket_booking.database.event_queries import EventQueries

from event_ticket_booking.models.event import Event

from event_ticket_booking.utils import exceptions

class EventService:
    def __init__(self, db_file):
        self.db_file = db_file
        self.event_queries = EventQueries(self.db_file)


    def create_event(self, title, event_price, location, date_time, total_seats):
        event = Event(title, event_price, location, date_time, total_seats)
        event_id = self.event_queries.add_event(title=event.title, event_price=event.event_price, location=event.location, date_time=event.date_time, total_seats=event.total_seats)
        if event_id:
            return event_id
        else:
            raise exceptions.BookingError
        
    def get_one_event(self, event_id):
        event = self.event_queries.get_event_by_id(event_id=event_id)
        if event:
            return event
        else:
            raise exceptions.EventDoesNotExistsError
        
    
    def get_events(self):
        return self.event_queries.get_all_event()
    
    def delete(self, event_id):
        if self.get_one_event(event_id=event_id):
            return self.event_queries.remove_event(event_id=event_id)

    def check_availability(self, event_id):
        event = self.get_one_event(event_id=event_id)
        return event[5] > 0
    
    def close(self):
        self.event_queries.close_connection()