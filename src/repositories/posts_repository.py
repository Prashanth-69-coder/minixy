import time

from supabase import create_client
from dotenv import load_dotenv

class PostsRepository:
    def __init__(self):
        load_dotenv()
        supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDc4NjgxNCwiZXhwIjoyMDY2MzYyODE0fQ.QinJdPz9s_PSei13oqzgxS6f6yoFmagHEn_svKVvbVg"

        self.supabase = create_client(supabase_url,supabase_key)

    def upload_file(self, selected_files, user_id):
        urls = []
        for selected_image in selected_files:
            file_name = f"{selected_image.filename}_{time.time()}"
            file_bytes = selected_image.file.read()
            self.supabase.storage.from_("posts").upload(file_name, file_bytes)
            url = self.supabase.storage.from_("posts").get_public_url(file_name)
            urls.append(url)
        return urls

    def create_post(self,post):
        res = self.supabase.table('posts').upsert(post).execute()
        return res.data

    def update_post(self,post,post_id):
        res = self.supabase.table('posts').update(post).eq('id',post_id).execute()
        return res.data

    def reterive_posts(self):
        res = self.supabase.table('posts').select('*').order('created_at', desc=True).execute()
        if res:
            return res.data
        else:
            return None

    def user_posts(self,user_id):
        res =  self.supabase.table('posts').select('*').eq('user_id',user_id).execute()
        return res.data








