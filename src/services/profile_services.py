from ..repositories.profile_repository import ProfileRepository

class ProfileService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
    
    def create_user_profile(self, id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture=None):
        res = self.profile_repo.create_user_profile(id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture)
        return res
    
    def get_user_profile(self, id):
        res = self.profile_repo.get_user_profile(id)
        return res
    
    def update_user_profile(self, id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture=None):
        res = self.profile_repo.update_user_profile(id, user_name, first_name, last_name, role, bio, skills, experience, profile_picture)
        return res