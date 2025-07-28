from supabase import create_client
from dotenv import load_dotenv

class StudentRepository:
    def __init__(self):
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(supabase_url, supabase_key)

    def list_visible_jobs(self, current_user_id=None):
        """Get all visible jobs for students to browse, excluding current user's jobs"""
        if current_user_id:
            result = self.supabase.table('jobs').select('*').eq('visible', True).neq('posted_by', current_user_id).order('created_at', desc=True).execute()
        else:
            result = self.supabase.table('jobs').select('*').eq('visible', True).order('created_at', desc=True).execute()
        return result.data

    def get_job(self, job_id):
        """Get a specific job by ID"""
        result = self.supabase.table('jobs').select('*').eq('id', job_id).execute()
        if result.data:
            return result.data[0]
        return None

    def get_jobs_by_company(self, company):
        """Get jobs filtered by company"""
        result = self.supabase.table('jobs').select('*').eq('visible', True).eq('company', company).execute()
        return result.data

    def get_jobs_by_location(self, location):
        """Get jobs filtered by location"""
        result = self.supabase.table('jobs').select('*').eq('visible', True).eq('location', location).execute()
        return result.data

    def search_jobs(self, search_term):
        """Search jobs by title, description, or company"""
        result = self.supabase.table('jobs').select('*').eq('visible', True).or_(f'title.ilike.%{search_term}%,description.ilike.%{search_term}%,company.ilike.%{search_term}%').execute()
        return result.data 