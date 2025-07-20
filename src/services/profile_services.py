from ..repositories.profile_repository import ProfileRepository

class ProfileService:
    def __init__(self):
        self.profile_repo = ProfileRepository()
    
    def create_user_profile(self,profile):
        res = self.profile_repo.create_profile(profile)
        return res

    def get_profile(self,user_id):
        res = self.profile_repo.get_profile(user_id)
        return res

    def get_role(self,user_id):
        res = self.profile_repo.get_role(user_id)
        return res