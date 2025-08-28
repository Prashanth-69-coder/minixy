import os
from supabase import create_client
from dotenv import load_dotenv

class AuthRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

        # Create client
        self.supabase = create_client(supabase_url, supabase_key)

    def signup_user(self, email, password):
        try:
            # Sign up user with Supabase - auto confirm email for simplified flow
            user = self.supabase.auth.sign_up({
                'email': email,
                'password': password
            })
            return user
        except Exception as e:
            return None

    def login_user(self, email, password):
        try:
            result = self.supabase.auth.sign_in_with_password({'email': email, 'password': password})
            return result
        except Exception as e:
            return None
    
    def current_user(self, session_token):
        if not session_token:
            return None
            
        try:
            user = self.supabase.auth.get_user(session_token)
            return user
        except Exception as e:
            return None

    def logout_user(self):
        try:
            self.supabase.auth.sign_out()
            return True
        except Exception as e:
            return False

    def refresh_token(self, refresh_token):
        try:
            result = self.supabase.auth.refresh_session(refresh_token)
            return result
        except Exception as e:
            return None

    def reset_password(self, email):
        try:
            self.supabase.auth.reset_password_email(email)
            return True
        except Exception as e:
            return False

    def update_password(self, token, password):
        try:
            result = self.supabase.auth.update_user({'password': password})
            return result
        except Exception as e:
            return None

    def get_user_by_email(self, email):
        try:
            result = self.supabase.table('profiles').select('*').eq('id', email).single().execute()
            return result.data if result.data else None
        except Exception as e:
            return None






