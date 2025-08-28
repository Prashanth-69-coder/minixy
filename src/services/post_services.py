from ..repositories.posts_repository import PostsRepository

class PostServices:
    def __init__(self):
        self.post_repo = PostsRepository()

    def create_post(self,post):
        res = self.post_repo.create_post(post)
        return res

    def update_post(self, post, post_id):
        res = self.post_repo.update_post(post, post_id)
        return res.data

    def reterive_posts(self):
        res = self.post_repo.reterive_posts()
        return res

    def reterive_posts_with_engagement(self, limit=5):
        res = self.post_repo.reterive_posts_with_engagement(limit)
        return res

    def reterive_posts_newest(self, limit=5):
        res = self.post_repo.reterive_posts_newest(limit)
        return res

    def reterive_posts_trending(self, limit=5):
        res = self.post_repo.reterive_posts_trending(limit)
        return res

    def reterive_posts_by_filter(self, filter_type="newest", limit=5):
        res = self.post_repo.reterive_posts_by_filter(filter_type, limit)
        return res

    def search_posts(self, query, limit=5):
        res = self.post_repo.search_posts(query, limit)
        return res

    def reterive_posts_by_role(self, role, limit=5):
        res = self.post_repo.reterive_posts_by_role(role, limit)
        return res

    def get_post_by_id(self, post_id):
        return self.post_repo.get_post_by_id(post_id)

    def update_post_content(self, post_id, user_id, title, description):
        if not title.strip() or not description.strip():
            return {'success': False, 'error': 'Title and description are required'}
        
        # Check ownership
        if not self.post_repo.check_post_ownership(post_id, user_id):
            return {'success': False, 'error': 'You can only edit your own posts'}
        
        result = self.post_repo.update_post_content(post_id, user_id, title.strip(), description.strip())
        return {'success': result is not None, 'post': result}

    def delete_post(self, post_id, user_id):
        # Check ownership
        if not self.post_repo.check_post_ownership(post_id, user_id):
            return {'success': False, 'error': 'You can only delete your own posts'}
        
        success = self.post_repo.delete_post(post_id, user_id)
        return {'success': success}

    def check_post_ownership(self, post_id, user_id):
        return self.post_repo.check_post_ownership(post_id, user_id)

    def user_posts(self,user_id):
        res = self.post_repo.user_posts(user_id)
        return res.data

