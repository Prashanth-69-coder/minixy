from supabase import create_client


class MessagesRepository:
    def __init__(self):
        self.supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MDc4NjgxNCwiZXhwIjoyMDY2MzYyODE0fQ.QinJdPz9s_PSei13oqzgxS6f6yoFmagHEn_svKVvbVg"
        self.supabase = create_client(self.supabase_url,self.supabase_key)


    def create_message(self, conversation_id, sender_id, content):
        res = self.supabase.table('messages').insert({
            'conversation_id': conversation_id,
            'sender_id': sender_id,
            'content': content
        }).execute()
        return res.data

    def get_messages(self,conversation_id):
        res = self.supabase.table('messages').select('*').eq('conversation_id',conversation_id).execute()
        return res.data

    

    