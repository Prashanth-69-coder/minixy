from ..repositories.comments_repository import CommentsRepository
from ..repositories.profile_repository import ProfileRepository

class CommentsService:
    def __init__(self):
        self.comments_repository = CommentsRepository()
        self.profile_repository = ProfileRepository()

    def create_comment(self, user_id, post_id, content):
        if not content or not content.strip():
            return {'success': False, 'error': 'Comment content cannot be empty'}
        
        comment = self.comments_repository.create_comment(user_id, post_id, content.strip())
        return {'success': comment is not None, 'comment': comment}

    def get_post_comments_with_profiles(self, post_id):
        comments = self.comments_repository.get_post_comments(post_id)
        
        if not comments:
            return []
        
        # Get unique user IDs to minimize profile queries
        user_ids = list(set(comment['user_id'] for comment in comments))
        
        # Batch fetch all required profiles in one query
        profiles_dict = self.profile_repository.get_profiles_batch(user_ids)
        
        # Enhance comments with profile data
        enhanced_comments = []
        for comment in comments:
            profile = profiles_dict.get(comment['user_id'], {})
            enhanced_comment = comment.copy()
            enhanced_comment['author_first_name'] = profile.get('first_name', 'Unknown')
            enhanced_comment['author_last_name'] = profile.get('last_name', '')
            enhanced_comment['author_role'] = profile.get('role', 'User')
            enhanced_comments.append(enhanced_comment)
        
        return enhanced_comments

    def get_post_comments_count(self, post_id):
        return self.comments_repository.get_post_comments_count(post_id)

    def get_posts_comments_count_batch(self, post_ids):
        return self.comments_repository.get_posts_comments_count_batch(post_ids)

    def update_comment(self, comment_id, user_id, content):
        if not content or not content.strip():
            return {'success': False, 'error': 'Comment content cannot be empty'}
        
        comment = self.comments_repository.get_comment_by_id(comment_id)
        if not comment or comment.get('user_id') != user_id:
            return {'success': False, 'error': 'Comment not found or unauthorized'}
        
        updated_comment = self.comments_repository.update_comment(comment_id, content.strip())
        return {'success': updated_comment is not None, 'comment': updated_comment}

    def delete_comment(self, comment_id, user_id):
        comment = self.comments_repository.get_comment_by_id(comment_id)
        if not comment or comment.get('user_id') != user_id:
            return {'success': False, 'error': 'Comment not found or unauthorized'}
        
        success = self.comments_repository.delete_comment(comment_id, user_id)
        return {'success': success}