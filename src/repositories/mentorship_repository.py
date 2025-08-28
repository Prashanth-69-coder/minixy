from supabase import create_client
from typing import List, Optional, Dict, Any

class MentorshipRepository:
    def __init__(self):
        self.supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDc4NjgxNCwiZXhwIjoyMDY2MzYyODE0fQ.QinJdPz9s_PSei13oqzgxS6f6yoFmagHEn_svKVvbVg"
        self.supabase = create_client(self.supabase_url,self.supabase_key)

    def create_mentorship(self, mentorship):
        # Since mentorships table doesn't exist, return None
        return None

    def create_mentor_request(self, requester_id, receiver_id, description):
        res = self.supabase.table('mentor_requests').insert({
            'requester_id': requester_id,
            'receiver_id': receiver_id,
            'description': description,
            'status': 'pending'
        }).execute()
        return res.data
    
    def get_mentor_requests_for_alumni(self, alumni_id: str) -> List[Dict[Any, Any]]:
        """Get all mentorship requests received by an alumni"""
        try:
            res = self.supabase.table('mentor_requests').select('*').eq('receiver_id', alumni_id).order('created_at', desc=True).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching mentor requests: {e}")
            return []
    
    def get_mentor_requests_sent_by_student(self, student_id: str) -> List[Dict[Any, Any]]:
        """Get all mentorship requests sent by a student"""
        try:
            res = self.supabase.table('mentor_requests').select('*').eq('requester_id', student_id).order('created_at', desc=True).execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching sent requests: {e}")
            return []
    
    def update_mentor_request_status(self, request_id: str, status: str) -> Optional[Dict[Any, Any]]:
        """Update the status of a mentor request (accept/reject)"""
        try:
            res = self.supabase.table('mentor_requests').update({
                'status': status
            }).eq('id', request_id).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error updating request status: {e}")
            return None
    
    def get_mentor_request_by_id(self, request_id: str) -> Optional[Dict[Any, Any]]:
        """Get a specific mentor request by ID"""
        try:
            res = self.supabase.table('mentor_requests').select('*').eq('id', request_id).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            print(f"Error fetching request: {e}")
            return None
    
    def set_mentor_availability(self, alumni_id: str, available: bool) -> bool:
        """Set mentor availability status for an alumni"""
        try:
            res = self.supabase.table('profiles').update({
                'mentor_available': available
            }).eq('id', alumni_id).execute()
            return True
        except Exception as e:
            print(f"Error updating mentor availability: {e}")
            return False
    
    def get_available_mentors(self, expertise_filter: Optional[str] = None, search_query: Optional[str] = None) -> List[Dict[Any, Any]]:
        """Get list of available mentors with optional filtering"""
        try:
            query = self.supabase.table('profiles').select('*').eq('role', 'alumni').eq('mentor_available', True)
            
            if expertise_filter and expertise_filter != 'All Expertise':
                query = query.contains('skills', [expertise_filter])
            
            if search_query:
                # Search in name, headline, or skills
                query = query.or_(f'first_name.ilike.%{search_query}%,last_name.ilike.%{search_query}%,headline.ilike.%{search_query}%')
            
            res = query.execute()
            return res.data if res.data else []
        except Exception as e:
            print(f"Error fetching available mentors: {e}")
            return []
    
    def get_mentorship_statistics(self, alumni_id: str) -> Dict[str, int]:
        """Get mentorship statistics for an alumni"""
        try:
            # Count pending requests
            pending_res = self.supabase.table('mentor_requests').select('id', count='exact').eq('receiver_id', alumni_id).eq('status', 'pending').execute()
            pending_count = pending_res.count if pending_res.count else 0
            
            # Count accepted requests
            accepted_res = self.supabase.table('mentor_requests').select('id', count='exact').eq('receiver_id', alumni_id).eq('status', 'accepted').execute()
            accepted_count = accepted_res.count if accepted_res.count else 0
            
            return {
                'pending_requests': pending_count,
                'accepted_requests': accepted_count,
                'active_mentorships': 0,  # Since mentorships table doesn't exist
                'total_requests': pending_count + accepted_count
            }
        except Exception as e:
            print(f"Error fetching statistics: {e}")
            return {'pending_requests': 0, 'accepted_requests': 0, 'active_mentorships': 0, 'total_requests': 0}
    
    def create_mentorship_from_request(self, request_id: str, mentor_id: str, mentee_id: str) -> Optional[Dict[Any, Any]]:
        """Create an active mentorship relationship from an accepted request"""
        try:
            # Since mentorships table doesn't exist, we'll just return None
            # but we could update the mentor_requests table instead
            return None
        except Exception as e:
            print(f"Error creating mentorship: {e}")
            return None