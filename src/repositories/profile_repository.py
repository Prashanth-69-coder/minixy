from supabase import create_client
import os
from dotenv import load_dotenv

class ProfileRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
            
        self.supabase = create_client(supabase_url,supabase_key)

    def create_profile(self, profile):
        res = self.supabase.table('profiles').upsert(profile).execute()
        return res.data

    def create_user_profile(self, profile):
        res = self.supabase.table('profiles').upsert(profile).execute()
        return res.data
        
    def get_profile(self,user_id):
        result = self.supabase.table('profiles').select('*').eq('id',user_id).execute()
        return result.data

    def get_role(self,user_id):
        result = self.supabase.table('profiles').select('role').eq('id',user_id).execute()
        return result.data

    def get_all_alumni(self, current_user_id=None):
        if current_user_id:
            result = self.supabase.table('profiles').select('*').eq('role', 'alumni').neq('id', current_user_id).execute()
        else:
            result = self.supabase.table('profiles').select('*').eq('role', 'alumni').execute()
        return result.data

    def get_all_students(self, current_user_id=None):
        if current_user_id:
            result = self.supabase.table('profiles').select('*').eq('role', 'student').neq('id', current_user_id).execute()
        else:
            result = self.supabase.table('profiles').select('*').eq('role', 'student').execute()
        return result.data

    def get_profiles_batch(self, user_ids):
        if not user_ids:
            return {}
        
        result = self.supabase.table('profiles').select('*').in_('id', user_ids).execute()
        return {profile['id']: profile for profile in result.data}

    def update_user_profile(self, profile):
        try:
            result = self.supabase.table('profiles').update(profile).eq('id', profile['id']).execute()
            return result.data[0] if result.data else None
        except Exception as e:
            return None

    def update_profile(self, profile_data):
        try:
            res = self.supabase.table('profiles').update(profile_data).eq('id', profile_data['id']).execute()
            return res.data[0] if res.data else None
        except Exception as e:
            return None
