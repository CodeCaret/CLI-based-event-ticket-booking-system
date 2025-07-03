class BookingError(Exception):
    pass

# User related errors

class UserAlreadyExistsError(BookingError):
    def __init__(self, message = 'User with this email already exists'):
        super().__init__(message)

class UserNotFoundError(BookingError):
    def __init__(self, message = "User with this email doesn't exists"):
        super().__init__(message)

class IncorrectPasswordError(BookingError):
    def __init__(self, message = "Incorrect Password"):
        super().__init__(message)



# EventEventDoesNot related errors

class EventDoesNotExistsError(BookingError):
    def __init__(self, message = "Event with this id doesn't exists"):
        super().__init__(message)


class TicketNotFoundError(BookingError):
    def __init__(self, message = "Ticket with this id doesn't exists"):
        super().__init__(message)