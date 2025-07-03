from supabase import create_client
from dotenv import load_dotenv

class ProfileRepository:
    def __init__(self):
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(supabase_url,supabase_key)


    def create_user_profile(self, id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture=None):
        user_profile = self.supabase.table('profiles').insert({
            'id': id,
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'bio': bio,
            'skills': skills,
            'experience': experience,
            'profile_picture': profile_picture
        }).execute()
        return user_profile

    def get_user_profile(self, id):
        user_profile = self.supabase.table('profiles').select('*').eq('id', id).single().execute()
        return user_profile

    def update_user_profile(self, id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture=None):
        user_profile = self.supabase.table('profiles').update({
            'user_name': user_name,
            'first_name': first_name,
            'last_name': last_name,
            'role': role,
            'bio': bio,
            'skills': skills,
            'experience': experience,
            'profile_picture': profile_picture
        }).eq('id', id).execute()
        return user_profile
        