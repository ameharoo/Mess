
from ini_parser import MessageIniParser
from message_manager import MessageManager
import message
from backend import Backend


class Generator:
    message_manager: MessageManager
    ini_parser: MessageIniParser

    builtin_types: [message.Message] = [
        message.Int8(),
        message.Int16(),
        #"Int32": message.Int32,
        #"Float": message.Float,
        #"Fixed16": message.Fixed16,
        #"Fixed32": message.Fixed32,
        message.Message("VarArray", [
            message.MessageField("length", "Int16"),
        ], ["T"]),
    ]

    def __init__(self, backend: Backend):
        self.backend = backend

        self.message_manager = MessageManager()
        self.populate_builtin_types()

        self.ini_parser = MessageIniParser()
        self.sorted_messages = []

    def populate_builtin_types(self):
        for message in self.builtin_types:
            self.message_manager.register(message)

    def load_file(self, filename: str):
        self.ini_parser.load_file(filename)

        for message_data in self.ini_parser.messages:
            name, gen_args = self.message_manager.deserialize_message_name(message_data.name)
            fields = [message.MessageField(field_data.name, field_data.type, field_data.docs) for field_data in message_data.fields]
            self.message_manager.register(message.Message(name, fields, generic_args=gen_args, docs=message_data.docs))

    def render_message(self, obj: message.Message):
        return self.backend.render_message(obj)

    def resolve_dependencies(self):
        self.message_manager.resolve_dependencies()

    def write_to_file(self, filename: str):
        self.resolve_dependencies()

        print(f"** Render protocol")
        with open(filename, "w") as output:
            for message in self.message_manager.get_all():
                if message.generic_args and self.message_manager.get(message.name):
                    # This is generic base
                    continue
                
                message_code = self.render_message(message)
                if message_code:
                    print(f"Successfully rendered {message.get_serialized_message_name()}")
                    output.write(message_code + "\n")
                else:
                    print(f"Empty {message.get_serialized_message_name()}")
