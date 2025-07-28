from ..repositories.conversations_repository import ConversationsRepository

class ConversationsService:
    def __init__(self):
        self.conv_repo = ConversationsRepository()

    def get_or_create_conversation(self, sender_id, receiver_id):
        return self.conv_repo.get_or_create_conversation(sender_id, receiver_id)

    def get_conversation(self, conversation_id):
        return self.conv_repo.get_conversation(conversation_id)

    def get_user_conversations(self, user_id):
        return self.conv_repo.get_user_conversations(user_id) 