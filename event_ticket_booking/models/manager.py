from event_ticket_booking.models.person import Person

class Manager(Person):
    def __init__(self, name, email, password, is_admin = 1):
        super().__init__(name, email, password, is_admin)