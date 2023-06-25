import typing


class MessageManager:
    defined_messages: dict[str, typing.Type]

    def __init__(self):
        self.defined_messages = {}

    def register(self, type_name: str, message: typing.Type):
        self.defined_messages[type_name] = message

    def get_all(self):
        return self.defined_messages

    def get(self, type_name):
        return self.defined_messages.get(type_name, None)


global_message_manager = MessageManager()
