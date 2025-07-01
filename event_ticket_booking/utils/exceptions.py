class BookingError(Exception):
    pass

# User related errors

class UserAlreadyExistsError(BookingError):
    def __init__(self, message = 'User with this email already exists'):
        super().__init__(message)