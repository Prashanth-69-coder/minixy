from supabase import create_client

class AluminiJobsRepository:
    def __init__(self):
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(supabase_url, supabase_key)

    def create_job(self, job):
        res = self.supabase.table('jobs').insert(job).execute()
        return res.data

    def list_visible_jobs(self, current_user_id=None):
        if current_user_id:
            res = self.supabase.table('jobs').select('*').eq('visible', True).neq('posted_by', current_user_id).execute()
        else:
            res = self.supabase.table('jobs').select('*').eq('visible', True).execute()
        return res.data

    def get_job(self, job_id):
        res = self.supabase.table('jobs').select('*').eq('id', job_id).single().execute()
        return res.data if hasattr(res, 'data') else None




