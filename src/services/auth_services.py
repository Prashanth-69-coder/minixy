from ..repositories.auth_repository import AuthRepository
from supabase import Client

class AuthService:
    def __init__(self):
        self.auth_repository = AuthRepository()

    def signup_user(self, email, password):
        return self.auth_repository.signup_user(email, password)

    def login_user(self, email, password):
        return self.auth_repository.login_user(email, password)

    def current_user(self, token):
        return self.auth_repository.supabase.auth.get_user(token)

    def get_user_by_email(self, email):
        return self.auth_repository.get_user_by_email(email)

    def logout_user(self):
        return self.auth_repository.logout_user()

    def refresh_token(self, refresh_token):
        return self.auth_repository.refresh_token(refresh_token)

    def reset_password(self, email):
        return self.auth_repository.reset_password(email)

    def update_password(self, token, password):
        return self.auth_repository.update_password(token, password)