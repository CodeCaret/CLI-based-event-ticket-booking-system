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