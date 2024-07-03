import uuid

class ContextManager:
    def __init__(self):
        self.user_contexts = {}

    def get_user_context(self, user_id):
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = {"messages": []}
        return self.user_contexts[user_id]

    def add_message(self, user_id, message):
        context = self.get_user_context(user_id)
        context["messages"].append(message)

    def generate_user_id(self):
        return str(uuid.uuid4())

context_manager = ContextManager()
