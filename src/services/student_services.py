from ..repositories.student_repository import StudentRepository

class StudentService:
    def __init__(self):
        self.student_repository = StudentRepository()

    def get_all_jobs(self, current_user_id):
        return self.student_repository.get_all_jobs(current_user_id)

    def get_job_by_id(self, job_id):
        return self.student_repository.get_job_by_id(job_id)

    def list_visible_jobs(self, current_user_id):
        return self.student_repository.list_visible_jobs(current_user_id)

    def get_job(self, job_id):
        return self.student_repository.get_job(job_id)

    def search_jobs(self, query, current_user_id):
        return self.student_repository.search_jobs(query, current_user_id)

    def get_jobs_by_company(self, company, current_user_id):
        return self.student_repository.get_jobs_by_company(company, current_user_id)

    def get_jobs_by_location(self, location, current_user_id):
        return self.student_repository.get_jobs_by_location(location, current_user_id)
