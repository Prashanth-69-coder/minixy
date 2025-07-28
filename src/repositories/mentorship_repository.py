from supabase import create_client

class MentorshipRepository:
    def __init__(self):
        self.supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(self.supabase_url,self.supabase_key)

    def create_mentorship(self,mentorship):
        res = self.supabase.table('mentorships').insert(mentorship).execute()
        return res.data

    def create_mentor_request(self, requester_id, receiver_id, description):
        res = self.supabase.table('mentor_requests').insert({
            'requester_id': requester_id,
            'receiver_id': receiver_id,
            'description': description
        }).execute()
        return res.data

    