from event_ticket_booking.database.user_queries import UserQueries

from event_ticket_booking.models.manager import Manager
from event_ticket_booking.models.user import User

from event_ticket_booking.utils.exceptions import (UserAlreadyExistsError,
                                                UserNotFoundError,
                                                IncorrectPasswordError)


class UserService:

    def __init__(self, db_file):
        self.db_file = db_file
        self.user_queries = UserQueries(self.db_file)

    def register_manager(self, name, email, password):
        manager = Manager(name, email, password)
        manager_id = self.user_queries.add_user(name=manager.name, email=manager.email, password=manager.password, is_admin=manager.is_admin)
        if manager_id:
            return manager_id
        else:
            raise UserAlreadyExistsError

    def register_user(self, name, email, password):
        user = User(name, email, password)
        user_id = self.user_queries.add_user(name=user.name, email=user.email, password=user.password, is_admin=user.is_admin)
        if user_id:
            return user_id
        else:
            raise UserAlreadyExistsError


    def login_user(self, email, password):
        user = self.get_user_by_email(email=email)
        if password == user[3]:
            return True
        else:
            raise IncorrectPasswordError


    def get_user_by_email(self, email):
        user = self.user_queries.get_user(email=email)
        if user:
            return user
        else:
            raise UserNotFoundError
        
    def check_manager(self, email):
        user = self.get_user_by_email(email=email)
        if user[4]:
            return True
        
    def check_user(self, email):
        user = self.get_user_by_email(email=email)
        if not user[4]:
            return True