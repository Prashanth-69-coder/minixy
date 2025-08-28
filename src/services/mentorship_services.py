from ..repositories.mentorship_repository import MentorshipRepository
from ..services.notifications_services import NotificationsService
from typing import List, Optional, Dict, Any

class MentorshipService:
    def __init__(self):
        self.mentorship_repo = MentorshipRepository()
        self.notifications_service = NotificationsService()

    def create_mentor_request(self, sender_id, receiver_id, description):
        """Create a new mentor request and send notification"""
        try:
            # Create the request
            request = self.mentorship_repo.create_mentor_request(sender_id, receiver_id, description)
            
            # Send notification to the receiver with requester's name
            if request:
                from ..services.profile_services import ProfileService
                profile_service = ProfileService()
                
                # Get requester's profile for notification
                requester_profile = profile_service.get_profile(sender_id)
                requester_name = "Someone"
                if requester_profile and len(requester_profile) > 0:
                    profile = requester_profile[0]
                    requester_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
                    if not requester_name:
                        requester_name = "Someone"
                
                self.notifications_service.create_mentorship_request_notification(
                    sender_id, receiver_id, requester_name
                )
            
            return request
        except Exception as e:
            print(f"Error creating mentor request: {e}")
            return None

    def create_mentorship(self, mentorship):
        """Create a new mentorship relationship"""
        return self.mentorship_repo.create_mentorship(mentorship)
    
    def get_mentor_requests_for_alumni(self, alumni_id: str) -> List[Dict[Any, Any]]:
        """Get all mentorship requests for an alumni with requester profiles"""
        try:
            requests = self.mentorship_repo.get_mentor_requests_for_alumni(alumni_id)
            
            # Enrich with requester profile data
            from ..services.profile_services import ProfileService
            profile_service = ProfileService()
            
            enriched_requests = []
            for request in requests:
                requester_profile = profile_service.get_profile(request['requester_id'])
                if requester_profile:
                    request['requester_profile'] = requester_profile[0]
                else:
                    request['requester_profile'] = {
                        'first_name': 'Unknown',
                        'last_name': 'User',
                        'headline': 'Student'
                    }
                enriched_requests.append(request)
            
            return enriched_requests
        except Exception as e:
            print(f"Error fetching enriched requests: {e}")
            return []
    
    def get_mentor_requests_sent_by_student(self, student_id: str) -> List[Dict[Any, Any]]:
        """Get all mentorship requests sent by a student"""
        return self.mentorship_repo.get_mentor_requests_sent_by_student(student_id)
    
    def accept_mentor_request(self, request_id: str, alumni_id: str) -> Dict[str, Any]:
        """Accept a mentor request and create mentorship relationship"""
        try:
            # Get the request details
            request = self.mentorship_repo.get_mentor_request_by_id(request_id)
            if not request:
                return {'success': False, 'error': 'Request not found'}
            
            # Verify the alumni is the receiver
            if request['receiver_id'] != alumni_id:
                return {'success': False, 'error': 'Unauthorized'}
            
            # Update request status to accepted
            updated_request = self.mentorship_repo.update_mentor_request_status(request_id, 'accepted')
            if not updated_request:
                return {'success': False, 'error': 'Failed to update request'}
            
            # Send notification to requester
            from ..services.profile_services import ProfileService
            profile_service = ProfileService()
            
            # Get mentor's name for notification
            mentor_profile = profile_service.get_profile(alumni_id)
            mentor_name = "Your mentor"
            if mentor_profile and len(mentor_profile) > 0:
                profile = mentor_profile[0]
                mentor_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
                if not mentor_name:
                    mentor_name = "Your mentor"
            
            self.notifications_service.create_mentorship_acceptance_notification(
                alumni_id, request['requester_id'], mentor_name
            )
            
            return {
                'success': True, 
                'request': updated_request
            }
            
        except Exception as e:
            print(f"Error accepting request: {e}")
            return {'success': False, 'error': 'Internal server error'}
    
    def reject_mentor_request(self, request_id: str, alumni_id: str) -> Dict[str, Any]:
        """Reject a mentor request"""
        try:
            # Get the request details
            request = self.mentorship_repo.get_mentor_request_by_id(request_id)
            if not request:
                return {'success': False, 'error': 'Request not found'}
            
            # Verify the alumni is the receiver
            if request['receiver_id'] != alumni_id:
                return {'success': False, 'error': 'Unauthorized'}
            
            # Update request status to rejected
            updated_request = self.mentorship_repo.update_mentor_request_status(request_id, 'rejected')
            if not updated_request:
                return {'success': False, 'error': 'Failed to update request'}
            
            # Send notification to requester
            from ..services.profile_services import ProfileService
            profile_service = ProfileService()
            
            # Get mentor's name for notification
            mentor_profile = profile_service.get_profile(alumni_id)
            mentor_name = "The mentor"
            if mentor_profile and len(mentor_profile) > 0:
                profile = mentor_profile[0]
                mentor_name = f"{profile.get('first_name', '')} {profile.get('last_name', '')}".strip()
                if not mentor_name:
                    mentor_name = "The mentor"
            
            self.notifications_service.create_mentorship_rejection_notification(
                alumni_id, request['requester_id'], mentor_name
            )
            
            return {'success': True, 'request': updated_request}
            
        except Exception as e:
            print(f"Error rejecting request: {e}")
            return {'success': False, 'error': 'Internal server error'}
    
    def set_mentor_availability(self, alumni_id: str, available: bool) -> Dict[str, Any]:
        """Toggle mentor availability status"""
        try:
            success = self.mentorship_repo.set_mentor_availability(alumni_id, available)
            if success:
                return {'success': True, 'available': available}
            else:
                return {'success': False, 'error': 'Failed to update availability'}
        except Exception as e:
            print(f"Error updating availability: {e}")
            return {'success': False, 'error': 'Internal server error'}
    
    def get_available_mentors(self, expertise_filter: Optional[str] = None, search_query: Optional[str] = None) -> List[Dict[Any, Any]]:
        """Get list of available mentors with filtering"""
        return self.mentorship_repo.get_available_mentors(expertise_filter, search_query)
    
    def get_mentorship_statistics(self, alumni_id: str) -> Dict[str, int]:
        """Get comprehensive mentorship statistics for an alumni"""
        return self.mentorship_repo.get_mentorship_statistics(alumni_id)
 