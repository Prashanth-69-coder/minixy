from ..repositories.notifications_repository import NotificationsRepository
from ..repositories.profile_repository import ProfileRepository
from ..repositories.posts_repository import PostsRepository

class NotificationsService:
    def __init__(self):
        self.notifications_repository = NotificationsRepository()
        self.profile_repository = ProfileRepository()
        self.posts_repository = PostsRepository()

    def create_like_notification(self, post_id, liker_user_id):
        try:
            # Get post details to find the owner
            post = self.posts_repository.get_post_by_id(post_id)
            if not post:
                return {'success': False, 'error': 'Post not found'}
            
            post_owner_id = post['user_id']
            
            # Get liker's profile
            liker_profile = self.profile_repository.get_profile(liker_user_id)
            if not liker_profile or len(liker_profile) == 0:
                return {'success': False, 'error': 'Liker profile not found'}
            
            liker_name = f"{liker_profile[0].get('first_name', '')} {liker_profile[0].get('last_name', '')}".strip()
            if not liker_name:
                liker_name = "Someone"
            
            # Create notification
            notification = self.notifications_repository.create_like_notification(
                post_owner_id, liker_user_id, post_id, liker_name
            )
            
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_comment_notification(self, post_id, commenter_user_id):
        try:
            # Get post details to find the owner
            post = self.posts_repository.get_post_by_id(post_id)
            if not post:
                return {'success': False, 'error': 'Post not found'}
            
            post_owner_id = post['user_id']
            
            # Get commenter's profile
            commenter_profile = self.profile_repository.get_profile(commenter_user_id)
            if not commenter_profile or len(commenter_profile) == 0:
                return {'success': False, 'error': 'Commenter profile not found'}
            
            commenter_name = f"{commenter_profile[0].get('first_name', '')} {commenter_profile[0].get('last_name', '')}".strip()
            if not commenter_name:
                commenter_name = "Someone"
            
            # Create notification
            notification = self.notifications_repository.create_comment_notification(
                post_owner_id, commenter_user_id, post_id, commenter_name
            )
            
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def get_user_notifications(self, user_id, limit=20):
        notifications = self.notifications_repository.get_user_notifications(user_id, limit)
        return {'success': True, 'notifications': notifications}

    def get_unread_count(self, user_id):
        count = self.notifications_repository.get_unread_notifications_count(user_id)
        return {'success': True, 'count': count}

    def mark_notification_as_read(self, notification_id, user_id):
        result = self.notifications_repository.mark_notification_as_read(notification_id, user_id)
        return {'success': result is not None}

    def mark_all_as_read(self, user_id):
        success = self.notifications_repository.mark_all_notifications_as_read(user_id)
        return {'success': success}

    def delete_notification(self, notification_id, user_id):
        success = self.notifications_repository.delete_notification(notification_id, user_id)
        return {'success': success}
    
    def create_notification(self, user_id: str, title: str, message: str, type: str, related_id: str = None):
        """Create a generic notification for mentorship and other purposes"""
        try:
            notification = self.notifications_repository.create_notification(
                user_id=user_id,
                title=title,
                message=message,
                type=type,
                related_id=related_id
            )
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            print(f"Error creating notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_mentorship_request_notification(self, requester_id: str, receiver_id: str, requester_name: str):
        """Create notification for new mentorship request"""
        try:
            title = "New Mentorship Request"
            message = f"{requester_name} has sent you a mentorship request."
            
            notification = self.notifications_repository.create_notification(
                user_id=receiver_id,
                title=title,
                message=message,
                type="mentorship_request",
                related_id=requester_id
            )
            
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            print(f"Error creating mentorship request notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_mentorship_acceptance_notification(self, mentor_id: str, mentee_id: str, mentor_name: str):
        """Create notification for accepted mentorship request"""
        try:
            title = "Mentorship Request Accepted"
            message = f"{mentor_name} has accepted your mentorship request! You can now start your mentorship journey."
            
            notification = self.notifications_repository.create_notification(
                user_id=mentee_id,
                title=title,
                message=message,
                type="mentorship_accepted",
                related_id=mentor_id
            )
            
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            print(f"Error creating mentorship acceptance notification: {e}")
            return {'success': False, 'error': str(e)}
    
    def create_mentorship_rejection_notification(self, mentor_id: str, mentee_id: str, mentor_name: str):
        """Create notification for rejected mentorship request"""
        try:
            title = "Mentorship Request Update"
            message = f"{mentor_name} has reviewed your mentorship request. Consider reaching out to other mentors."
            
            notification = self.notifications_repository.create_notification(
                user_id=mentee_id,
                title=title,
                message=message,
                type="mentorship_rejected",
                related_id=mentor_id
            )
            
            return {'success': notification is not None, 'notification': notification}
        except Exception as e:
            print(f"Error creating mentorship rejection notification: {e}")
            return {'success': False, 'error': str(e)}