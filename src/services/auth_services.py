from ..repositories import auth_repository
from ..repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def signup_user(self,email,password):
        user = self.repository.signup_user(email,password)
        return user

    def login_user(self,email,password):
        user = self.repository.login_user(email,password)
        return user

    def current_user(self,session_token):
        user = self.repository.current_user(session_token)
        return user

    def get_user_by_email(self, email):
        return self.repository.get_user_by_email(email)
        
