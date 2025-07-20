from ..repositories.posts_repository import PostsRepository

class PostServices:
    def __init__(self):
        self.post_repo = PostsRepository()

    def create_post(self,post):
        res = self.post_repo.create_post(post)
        return res.data

    def update_post(self, post, post_id):
        res = self.post_repo.update_post(post, post_id)
        return res.data

    def reterive_posts(self):
        res = self.post_repo.reterive_posts()
        return res.data

    def user_posts(self,user_id):
        res = self.post_repo.user_posts(user_id)
        return res.data

