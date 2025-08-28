from ..repositories.reactions_repository import ReactionsRepository
from ..repositories.posts_repository import PostsRepository

class ReactionsService:
    def __init__(self):
        self.reactions_repository = ReactionsRepository()
        self.posts_repository = PostsRepository()

    def toggle_like(self, user_id, post_id):
        # Check if user is trying to like their own post
        post = self.posts_repository.get_post_by_id(post_id)
        if not post:
            return {'success': False, 'error': 'Post not found'}
        
        if post.get('user_id') == user_id:
            return {'success': False, 'error': 'Cannot like your own post'}
        
        # Get current reaction status
        existing_reaction = self.reactions_repository.get_user_reaction(user_id, post_id)
        
        if existing_reaction:
            # User has already liked the post, so remove the like
            success = self.reactions_repository.remove_reaction(user_id, post_id)
            if success:
                # Get updated count after removal
                engagement = self.reactions_repository.get_post_reactions_count(post_id)
                return {
                    'success': True, 
                    'action': 'removed', 
                    'liked': False,
                    'likes_count': engagement['likes_count']
                }
            else:
                return {'success': False, 'error': 'Failed to remove like'}
        else:
            # User hasn't liked the post, so add a like
            reaction = self.reactions_repository.add_reaction(user_id, post_id, 'like')
            if reaction:
                # Get updated count after addition
                engagement = self.reactions_repository.get_post_reactions_count(post_id)
                return {
                    'success': True, 
                    'action': 'added', 
                    'liked': True,
                    'likes_count': engagement['likes_count']
                }
            else:
                return {'success': False, 'error': 'Failed to add like'}

    def get_post_engagement(self, post_id):
        return self.reactions_repository.get_post_reactions_count(post_id)

    def get_posts_engagement_batch(self, post_ids):
        return self.reactions_repository.get_posts_reactions_batch(post_ids)

    def get_user_reactions_for_posts(self, user_id, post_ids):
        return self.reactions_repository.get_user_reactions_for_posts(user_id, post_ids)

    def check_user_liked_post(self, user_id, post_id):
        reaction = self.reactions_repository.get_user_reaction(user_id, post_id)
        return reaction is not None and reaction.get('reaction') == 'like'