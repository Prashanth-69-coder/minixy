from supabase import create_client


class ConversationsRepository:
    def __init__(self):
        self.supabase_url = "https://drkvofasyisiqdqxbegu.supabase.co"
        self.supabase_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRya3ZvZmFzeWlzaXFkcXhiZWd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTA3ODY4MTQsImV4cCI6MjA2NjM2MjgxNH0.2psBWqHo8qqFEdg4JimWWEFFWxsX1oHxR5pnOWg-5fI"
        self.supabase = create_client(self.supabase_url,self.supabase_key)

        def create_conversation(conversation):
            res = self.supabase.table('conversations').insert(conversation).execute()
            return res.data

        def get_conversation(conversation_id):
            res = self.supabase.table('conversations').select('*').eq('id',conversation_id).execute()
            return res.data

    def get_user_conversations(self, user_id):
        res = self.supabase.table('conversations').select('*').or_(
            f'sender_id.eq.{user_id},receiver_id.eq.{user_id}'
        ).execute()
        return res.data

    def get_or_create_conversation(self, sender_id, receiver_id):
        or_filter = (
            f"and(sender_id.eq.{sender_id},receiver_id.eq.{receiver_id}),"
            f"and(sender_id.eq.{receiver_id},receiver_id.eq.{sender_id})"
        )
        conv_query = self.supabase.table('conversations').select('*').or_(or_filter).execute()
        if conv_query.data and len(conv_query.data) > 0:
            return conv_query.data[0]['id']
        else:
            conv_res = self.supabase.table('conversations').insert({
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'is_group': False
            }).execute()
            return conv_res.data[0]['id']
            