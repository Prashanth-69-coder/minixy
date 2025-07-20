from supabase import create_client
from dotenv import load_dotenv

class ProfileRepository:
    def __init__(self):
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(supabase_url,supabase_key)

    def create_profile(self, profile):
        res = self.supabase.table('profiles').upsert(profile).execute()
        return res.data
    def get_profile(self,user_id):
        result = self.supabase.table('profiles').select('*').eq('id',user_id).execute()
        return result.data

    def get_role(self,user_id):
        result = self.supabase.table('profiles').select('role').eq('id',user_id).execute()
        return result.data








