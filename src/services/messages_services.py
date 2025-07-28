from ..repositories.messages_repository import MessagesRepository

class MessagesService:
    def __init__(self):
        self.messages_repo = MessagesRepository()

    def create_message(self, conversation_id, sender_id, content):
        return self.messages_repo.create_message(conversation_id, sender_id, content)

    def get_messages(self, conversation_id):
        return self.messages_repo.get_messages(conversation_id) 