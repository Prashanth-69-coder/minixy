from supabase import create_client
import os
from dotenv import load_dotenv
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AluminiJobsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
            
        self.supabase = create_client(supabase_url, supabase_key)

    def create_job(self, job):
        try:
            logger.debug(f"Creating job with data: {job}")
            res = self.supabase.table('jobs').insert(job).execute()
            logger.debug(f"Job creation response: {res}")
            return res.data
        except Exception as e:
            logger.error(f"Error creating job: {str(e)}")
            raise

    def list_visible_jobs(self, current_user_id=None):
        try:
            if current_user_id:
                res = self.supabase.table('jobs').select('*').eq('visible', True).neq('posted_by', current_user_id).execute()
            else:
                res = self.supabase.table('jobs').select('*').eq('visible', True).execute()
            return res.data
        except Exception as e:
            logger.error(f"Error listing jobs: {str(e)}")
            raise

    def get_jobs_by_user(self, user_id):
        """Get all jobs posted by a specific user"""
        try:
            res = self.supabase.table('jobs').select('*').eq('posted_by', user_id).execute()
            return res.data
        except Exception as e:
            logger.error(f"Error getting jobs by user: {str(e)}")
            raise

    def get_job(self, job_id):
        try:
            res = self.supabase.table('jobs').select('*').eq('id', job_id).single().execute()
            return res.data if hasattr(res, 'data') else None
        except Exception as e:
            logger.error(f"Error getting job: {str(e)}")
            raise

    def update_job_visibility(self, job_id, visible):
        """Update the visibility of a job"""
        try:
            res = self.supabase.table('jobs').update({'visible': visible}).eq('id', job_id).execute()
            return res.data
        except Exception as e:
            logger.error(f"Error updating job visibility: {str(e)}")
            raise