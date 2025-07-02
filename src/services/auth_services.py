from ..repositories import auth_repository
from ..repositories.auth_repository import AuthRepository


class AuthService:
    def __init__(self):
        self.repository = AuthRepository()

    def signup_user(self,email,password):
        return self.repository.signup_user(email,password)

    def login_user(self,email,password):
        return self.repository.login_user(email,password)


