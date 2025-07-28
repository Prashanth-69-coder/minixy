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

    def get_all_alumni(self, current_user_id=None):
        return self.profile_repo.get_all_alumni(current_user_id)

    def update_profile(self, profile_data):
        """Update user profile with new data"""
        try:
            res = self.profile_repo.update_profile(profile_data)
            return res
        except Exception as e:
            print(f"Error updating profile: {e}")
            raise e