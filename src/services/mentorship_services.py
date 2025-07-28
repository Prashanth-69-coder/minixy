from ..repositories.mentorship_repository import MentorshipRepository

class MentorshipService:
    def __init__(self):
        self.mentorship_repo = MentorshipRepository()

    def create_mentor_request(self, sender_id, receiver_id, description):
        return self.mentorship_repo.create_mentor_request(sender_id, receiver_id, description)

    def create_mentorship(self, mentorship):
        return self.mentorship_repo.create_mentorship(mentorship) 