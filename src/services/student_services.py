from ..repositories.student_repository import StudentRepository

class StudentServices:
    def __init__(self):
        self.student_repo = StudentRepository()

    def list_visible_jobs(self, current_user_id=None):
        """Get all visible jobs for students, excluding current user's jobs"""
        try:
            jobs = self.student_repo.list_visible_jobs(current_user_id)
            return jobs
        except Exception as e:
            print(f"Error listing jobs: {e}")
            return []

    def get_job(self, job_id):
        """Get a specific job by ID"""
        try:
            job = self.student_repo.get_job(job_id)
            return job
        except Exception as e:
            print(f"Error getting job: {e}")
            return None

    def search_jobs(self, search_term):
        """Search jobs by title, description, or company"""
        try:
            jobs = self.student_repo.search_jobs(search_term)
            return jobs
        except Exception as e:
            print(f"Error searching jobs: {e}")
            return []

    def get_jobs_by_company(self, company):
        """Get jobs filtered by company"""
        try:
            jobs = self.student_repo.get_jobs_by_company(company)
            return jobs
        except Exception as e:
            print(f"Error getting jobs by company: {e}")
            return []

    def get_jobs_by_location(self, location):
        """Get jobs filtered by location"""
        try:
            jobs = self.student_repo.get_jobs_by_location(location)
            return jobs
        except Exception as e:
            print(f"Error getting jobs by location: {e}")
            return [] 