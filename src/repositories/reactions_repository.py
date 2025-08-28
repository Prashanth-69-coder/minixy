import os
from supabase import create_client
from dotenv import load_dotenv

class ReactionsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

        self.supabase = create_client(supabase_url, supabase_key)

    def add_reaction(self, user_id, post_id, reaction_type="like"):
        try:
            # First check if reaction already exists
            existing = self.supabase.table('post_reactions').select('*').eq('user_id', user_id).eq('post_id', post_id).execute()
            
            if existing and existing.data:
                # Update existing reaction
                result = self.supabase.table('post_reactions').update({
                    'reaction': reaction_type
                }).eq('user_id', user_id).eq('post_id', post_id).execute()
            else:
                # Insert new reaction
                result = self.supabase.table('post_reactions').insert({
                    'user_id': user_id,
                    'post_id': post_id,
                    'reaction': reaction_type
                }).execute()
            
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def remove_reaction(self, user_id, post_id):
        try:
            result = self.supabase.table('post_reactions').delete().eq('user_id', user_id).eq('post_id', post_id).execute()
            return True
        except Exception as e:
            return False

    def get_user_reaction(self, user_id, post_id):
        try:
            result = self.supabase.table('post_reactions').select('*').eq('user_id', user_id).eq('post_id', post_id).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def get_post_reactions_count(self, post_id):
        try:
            result = self.supabase.table('post_reactions').select('*').eq('post_id', post_id).execute()
            reactions = result.data if result.data else []
            
            likes_count = len([r for r in reactions if r.get('reaction') == 'like'])
            
            return {
                'likes_count': likes_count,
                'total_reactions': len(reactions)
            }
        except Exception as e:
            return {'likes_count': 0, 'total_reactions': 0}

    def get_posts_reactions_batch(self, post_ids):
        try:
            if not post_ids:
                return {}
            
            result = self.supabase.table('post_reactions').select('*').in_('post_id', post_ids).execute()
            reactions = result.data if result.data else []
            
            reactions_by_post = {}
            for post_id in post_ids:
                post_reactions = [r for r in reactions if r.get('post_id') == post_id]
                reactions_by_post[post_id] = {
                    'likes_count': len([r for r in post_reactions if r.get('reaction') == 'like']),
                    'total_reactions': len(post_reactions)
                }
            
            return reactions_by_post
        except Exception as e:
            return {}

    def get_user_reactions_for_posts(self, user_id, post_ids):
        try:
            if not post_ids:
                return {}
            
            # Ensure post_ids are strings
            post_ids_str = [str(pid) for pid in post_ids]
            
            result = self.supabase.table('post_reactions').select('*').eq('user_id', str(user_id)).in_('post_id', post_ids_str).execute()
            reactions = result.data if result.data else []
            
            user_reactions = {}
            for reaction in reactions:
                user_reactions[reaction.get('post_id')] = reaction.get('reaction')
            
            return user_reactions
        except Exception as e:
            return {}