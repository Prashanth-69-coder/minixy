from supabase import create_client
from dotenv import load_dotenv

class PostsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(supabase_url,supabase_key)

        def create_jobs(jobs):
            res = self.supabase.table('jobs').upsert(jobs).execute()
            return res.data

        def update_jobs(jobs,jobs_id):
            res = self.supabase.table('jobs').update(jobs).eq('id',jobs_id).execute()
            return res.data

        def delete_jobs(jobs,job_id):
            res = self.supabase.table('jobs').delete(jobs).eq('id',job_id).execute()
            return res.data




