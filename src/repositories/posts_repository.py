import time
import os
from supabase import create_client
from dotenv import load_dotenv

class PostsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

        self.supabase = create_client(supabase_url,supabase_key)

    def upload_file(self, selected_files, user_id):
        urls = []
        for selected_image in selected_files:
            try:
                file_name = f"{selected_image.filename}_{time.time()}"
                file_bytes = selected_image.file.read()
                self.supabase.storage.from_("posts").upload(file_name, file_bytes)
                url = self.supabase.storage.from_("posts").get_public_url(file_name)
                urls.append(url)
            except Exception as e:
                continue
        return urls

    def create_post(self,post):
        res = self.supabase.table('posts').upsert(post).execute()
        return res.data

    def update_post(self,post,post_id):
        res = self.supabase.table('posts').update(post).eq('id',post_id).execute()
        return res.data

    def reterive_posts(self, limit=5):
        res = self.supabase.table('posts').select('*').order('created_at', desc=True).limit(limit).execute()
        if res:
            return res.data
        else:
            return None

    def reterive_posts_with_engagement(self, limit=5):
        posts = self.reterive_posts(limit)
        if not posts:
            return []
        
        post_ids = [post['id'] for post in posts]
        
        # Get likes count for each post
        likes_result = self.supabase.table('post_reactions').select('post_id').eq('reaction', 'like').in_('post_id', post_ids).execute()
        likes_data = likes_result.data if likes_result.data else []
        
        # Get comments count for each post
        comments_result = self.supabase.table('comments').select('post_id').in_('post_id', post_ids).execute()
        comments_data = comments_result.data if comments_result.data else []
        
        # Count engagement for each post
        for post in posts:
            post_id = post['id']
            post['likes_count'] = len([l for l in likes_data if l.get('post_id') == post_id])
            post['comments_count'] = len([c for c in comments_data if c.get('post_id') == post_id])
            post['shares_count'] = 0  # Placeholder for future implementation
        
        return posts

    def reterive_posts_newest(self, limit=5):
        res = self.supabase.table('posts').select('*').order('created_at', desc=True).limit(limit).execute()
        if res:
            return res.data
        else:
            return None

    def reterive_posts_trending(self, limit=5):
        # Reduced from 50 to 20 for better performance
        posts = self.supabase.table('posts').select('*').order('created_at', desc=True).limit(20).execute()
        if not posts or not posts.data:
            return []
        
        post_ids = [post['id'] for post in posts.data]
        
        # Get engagement data for trending calculation
        likes_result = self.supabase.table('post_reactions').select('post_id').eq('reaction', 'like').in_('post_id', post_ids).execute()
        likes_data = likes_result.data if likes_result.data else []
        
        comments_result = self.supabase.table('comments').select('post_id').in_('post_id', post_ids).execute()
        comments_data = comments_result.data if comments_result.data else []
        
        # Calculate trending score for each post
        for post in posts.data:
            post_id = post['id']
            likes_count = len([l for l in likes_data if l.get('post_id') == post_id])
            comments_count = len([c for c in comments_data if c.get('post_id') == post_id])
            
            # Simple trending algorithm: likes * 2 + comments * 3
            post['trending_score'] = (likes_count * 2) + (comments_count * 3)
            post['likes_count'] = likes_count
            post['comments_count'] = comments_count
            post['shares_count'] = 0
        
        # Sort by trending score and return top posts
        trending_posts = sorted(posts.data, key=lambda x: x.get('trending_score', 0), reverse=True)[:limit]
        return trending_posts

    def reterive_posts_by_filter(self, filter_type="newest", limit=5):
        if filter_type == "trending":
            return self.reterive_posts_trending(limit)
        else:  # Default to newest
            return self.reterive_posts_with_engagement(limit)

    def search_posts(self, query, limit=5):
        if not query or not query.strip():
            return self.reterive_posts_with_engagement(limit)
        
        search_term = f"%{query.strip()}%"
        res = self.supabase.table('posts').select('*').or_(f'title.ilike.{search_term},description.ilike.{search_term}').order('created_at', desc=True).limit(limit).execute()
        
        if res and res.data:
            posts = res.data
            post_ids = [post['id'] for post in posts]
            
            # Get engagement data
            likes_result = self.supabase.table('post_reactions').select('post_id').eq('reaction', 'like').in_('post_id', post_ids).execute()
            likes_data = likes_result.data if likes_result.data else []
            
            comments_result = self.supabase.table('comments').select('post_id').in_('post_id', post_ids).execute()
            comments_data = comments_result.data if comments_result.data else []
            
            # Add engagement counts
            for post in posts:
                post_id = post['id']
                post['likes_count'] = len([l for l in likes_data if l.get('post_id') == post_id])
                post['comments_count'] = len([c for c in comments_data if c.get('post_id') == post_id])
                post['shares_count'] = 0
            
            return posts
        else:
            return []

    def reterive_posts_by_role(self, role, limit=5):
        # Reduced from 50 to 15 for better performance
        posts_result = self.supabase.table('posts').select('*').order('created_at', desc=True).limit(15).execute()
        if not posts_result or not posts_result.data:
            return []
        
        posts = posts_result.data
        user_ids = list(set(post['user_id'] for post in posts))
        
        # Get profiles for these users and filter by role
        profiles_result = self.supabase.table('profiles').select('*').eq('role', role).in_('id', user_ids).execute()
        if not profiles_result or not profiles_result.data:
            return []
        
        role_user_ids = [profile['id'] for profile in profiles_result.data]
        
        # Filter posts by users with the specified role
        filtered_posts = [post for post in posts if post['user_id'] in role_user_ids][:limit]
        
        if filtered_posts:
            post_ids = [post['id'] for post in filtered_posts]
            
            # Get engagement data
            likes_result = self.supabase.table('post_reactions').select('post_id').eq('reaction', 'like').in_('post_id', post_ids).execute()
            likes_data = likes_result.data if likes_result.data else []
            
            comments_result = self.supabase.table('comments').select('post_id').in_('post_id', post_ids).execute()
            comments_data = comments_result.data if comments_result.data else []
            
            # Add engagement counts
            for post in filtered_posts:
                post_id = post['id']
                post['likes_count'] = len([l for l in likes_data if l.get('post_id') == post_id])
                post['comments_count'] = len([c for c in comments_data if c.get('post_id') == post_id])
                post['shares_count'] = 0
        
        return filtered_posts

    def get_post_by_id(self, post_id):
        try:
            result = self.supabase.table('posts').select('*').eq('id', post_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def update_post_content(self, post_id, user_id, title, description):
        try:
            result = self.supabase.table('posts').update({
                'title': title,
                'description': description,
                'updated_at': 'now()'
            }).eq('id', post_id).eq('user_id', user_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def delete_post(self, post_id, user_id):
        try:
            # First delete related comments
            self.supabase.table('comments').delete().eq('post_id', post_id).execute()
            
            # Delete related reactions
            self.supabase.table('post_reactions').delete().eq('post_id', post_id).execute()
            
            # Finally delete the post
            result = self.supabase.table('posts').delete().eq('id', post_id).eq('user_id', user_id).execute()
            return True
        except Exception as e:
            return False

    def check_post_ownership(self, post_id, user_id):
        try:
            result = self.supabase.table('posts').select('user_id').eq('id', post_id).eq('user_id', user_id).execute()
            return len(result.data) > 0 if result.data else False
        except Exception as e:
            return False

    def user_posts(self,user_id):
        res =  self.supabase.table('posts').select('*').eq('user_id',user_id).execute()
        return res.data








