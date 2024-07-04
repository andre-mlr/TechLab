class ContextManager:
    def __init__(self):
        self.user_contexts = {}

    def add_message(self, user_id, message):
        if user_id not in self.user_contexts:
            self.user_contexts[user_id] = []
        self.user_contexts[user_id].append(message)

    def get_user_context(self, user_id):
        return "\n".join(self.user_contexts.get(user_id, []))

    def generate_user_id(self):
        import uuid
        return str(uuid.uuid4())

context_manager = ContextManager()
