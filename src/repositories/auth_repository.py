import os

from supabase import create_client
from dotenv import load_dotenv

class AuthRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"

        self.supabase = create_client(supabase_url,supabase_key)

    def signup_user(self,email,password):
        user = self.supabase.auth.sign_up({'email':email,'password':password})
        return user

    def login_user(self,email,password):
        user = self.supabase.auth.sign_in_with_password({'email':email,'password':password})
        return user
    
    def current_user(self,session_token):
        user = self.supabase.auth.get_user(session_token)
        return user

    def get_user_by_email(self, email):
        # Query the auth.users table in Supabase to get the user by email
        response = self.supabase.table('users').select('id').eq('email', email).single().execute()
        if response and response.data and 'id' in response.data:
            return response.data['id']
        return None







