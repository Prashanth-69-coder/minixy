import os

from supabase import create_client
from dotenv import load_dotenv

class AuthRepository:
    def __init__(self):
        load_dotenv()

        self.supabase = create_client(os.getenv("supabase_url"),os.getenv("supabase_key"))

    def signup_user(self,email,password):
        user = self.supabase.auth.sing_up({'email':email,'password':password})
        return user

    def login_user(self,email,password):
        user = self.supabase.auth.singin({'email':email,'password':password})
        return user







