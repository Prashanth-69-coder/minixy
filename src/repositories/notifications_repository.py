import os
from supabase import create_client
from dotenv import load_dotenv

class NotificationsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

        self.supabase = create_client(supabase_url, supabase_key)

    def create_notification(self, user_id, title, message, type="general", related_id=None):
        """Create a notification with optional related_id for linking to specific entities"""
        try:
            notification_data = {
                'user_id': user_id,
                'title': title,
                'message': message,
                'type': type,
                'is_read': False
            }
            
            if related_id:
                notification_data['related_id'] = related_id
                
            result = self.supabase.table('notifications').insert(notification_data).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            print(f"Error creating notification: {e}")
            return None

    def get_user_notifications(self, user_id, limit=20):
        try:
            result = self.supabase.table('notifications').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(limit).execute()
            return result.data if result.data else []
        except Exception as e:
            return []

    def get_unread_notifications_count(self, user_id):
        try:
            result = self.supabase.table('notifications').select('id').eq('user_id', user_id).eq('is_read', False).execute()
            return len(result.data) if result.data else 0
        except Exception as e:
            return 0

    def mark_notification_as_read(self, notification_id, user_id):
        try:
            result = self.supabase.table('notifications').update({
                'is_read': True
            }).eq('id', notification_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def mark_all_notifications_as_read(self, user_id):
        try:
            result = self.supabase.table('notifications').update({
                'is_read': True
            }).eq('user_id', user_id).eq('is_read', False).execute()
            return True
        except Exception as e:
            return False

    def delete_notification(self, notification_id, user_id):
        try:
            result = self.supabase.table('notifications').delete().eq('id', notification_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            return False

    def create_like_notification(self, post_owner_id, liker_user_id, post_id, liker_name):
        if post_owner_id == liker_user_id:
            return None  # Don't notify users about their own likes
        
        title = "New Like"
        message = f"{liker_name} liked your post"
        
        return self.create_notification(post_owner_id, title, message, "like")

    def create_comment_notification(self, post_owner_id, commenter_user_id, post_id, commenter_name):
        if post_owner_id == commenter_user_id:
            return None  # Don't notify users about their own comments
        
        title = "New Comment"
        message = f"{commenter_name} commented on your post"
        
        return self.create_notification(post_owner_id, title, message, "comment")