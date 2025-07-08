from event_ticket_booking.database.user_queries import UserQueries

from event_ticket_booking.models.manager import Manager
from event_ticket_booking.models.user import User

from event_ticket_booking.utils.exceptions import (UserAlreadyExistsError,
                                                UserNotFoundError,
                                                IncorrectPasswordError)

import bcrypt

class UserService:

    def __init__(self, db_file):
        self.db_file = db_file
        self.user_queries = UserQueries(self.db_file)

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())

    def register_manager(self, name, email, password):
        manager = Manager(name, email, password)
        hashed_password = self.hash_password(password=manager.password)
        manager_id = self.user_queries.add_user(name=manager.name, email=manager.email, password=hashed_password, is_admin=manager.is_admin)
        if manager_id:
            return manager_id
        else:
            raise UserAlreadyExistsError

    def register_user(self, name, email, password):
        user = User(name, email, password)
        hashed_password = self.hash_password(password=user.password)
        user_id = self.user_queries.add_user(name=user.name, email=user.email, password=hashed_password, is_admin=user.is_admin)
        if user_id:
            return user_id
        else:
            raise UserAlreadyExistsError


    def login_user(self, email, password):
        user = self.get_user_by_email(email=email)
        if bcrypt.checkpw(password=password.encode('utf-8'), hashed_password=user[3]):
            return user
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
        return user[4]== 1
        
    def check_user(self, email):
        user = self.get_user_by_email(email=email)
        return user[4] == 0
    
    def close(self):
        self.user_queries.close_connection()