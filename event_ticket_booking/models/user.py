from event_ticket_booking.models.person import Person

class User(Person):
    def __init__(self, name, email, password, is_admin = 0):
        super().__init__(name, email, password, is_admin)