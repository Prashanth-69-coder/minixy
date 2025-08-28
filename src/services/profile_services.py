from ..repositories.profile_repository import ProfileRepository

class ProfileService:
    def __init__(self):
        self.profile_repository = ProfileRepository()

    def create_user_profile(self, profile):
        return self.profile_repository.create_user_profile(profile)

    def get_profile(self, user_id):
        return self.profile_repository.get_profile(user_id)

    def get_role(self, user_id):
        return self.profile_repository.get_role(user_id)

    def get_all_alumni(self, current_user_id):
        return self.profile_repository.get_all_alumni(current_user_id)

    def get_all_students(self, current_user_id):
        return self.profile_repository.get_all_students(current_user_id)

    def update_profile(self, profile):
        return self.profile_repository.update_profile(profile)

    def get_profiles_batch(self, user_ids):
        return self.profile_repository.get_profiles_batch(user_ids)