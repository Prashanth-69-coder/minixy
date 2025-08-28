import os
from supabase import create_client
from dotenv import load_dotenv

class CommentsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

        self.supabase = create_client(supabase_url, supabase_key)

    def create_comment(self, user_id, post_id, content):
        try:
            result = self.supabase.table('comments').insert({
                'user_id': user_id,
                'post_id': post_id,
                'content': content
            }).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def get_post_comments(self, post_id):
        try:
            # Single optimized query with better ordering and limit
            result = self.supabase.table('comments').select(
                'id, user_id, post_id, content, created_at'
            ).eq('post_id', post_id).order('created_at', desc=False).limit(50).execute()
            return result.data if result.data else []
        except Exception as e:
            return []

    def get_post_comments_count(self, post_id):
        try:
            result = self.supabase.table('comments').select('id').eq('post_id', post_id).execute()
            return len(result.data) if result.data else 0
        except Exception as e:
            return 0

    def get_posts_comments_count_batch(self, post_ids):
        try:
            if not post_ids:
                return {}
            
            result = self.supabase.table('comments').select('post_id').in_('post_id', post_ids).execute()
            comments = result.data if result.data else []
            
            comments_count = {}
            for post_id in post_ids:
                comments_count[post_id] = len([c for c in comments if c.get('post_id') == post_id])
            
            return comments_count
        except Exception as e:
            return {}

    def update_comment(self, comment_id, content):
        try:
            result = self.supabase.table('comments').update({
                'content': content
            }).eq('id', comment_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def delete_comment(self, comment_id, user_id):
        try:
            result = self.supabase.table('comments').delete().eq('id', comment_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            return False

    def get_comment_by_id(self, comment_id):
        try:
            result = self.supabase.table('comments').select('*').eq('id', comment_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None