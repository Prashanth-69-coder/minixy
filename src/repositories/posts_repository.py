from supabase import create_client
from dotenv import load_dotenv

class PostsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"

        self.supabase = create_client(supabase_url,supabase_key)
#
    def create_post(self,post):
        res = self.supabase.table('posts').upsert(post).execute()
        return res.data

    def update_post(self,post,post_id):
        res = self.supabase.table('posts').update(post).eq('id',post_id).execute()
        return res.data

    def reterive_posts(self):
        res = self.supabase.table('posts').select('*').execute()
        return res.data

    def user_posts(self,user_id):
        res =  self.supabase.table('posts').select('*').eq('user_id',user_id).execute()
        return res.data








