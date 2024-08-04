import typing

import messages.base as messages_base

class MessageIniParser:
    messages: list[messages_base.Message]
    protocol_name: str
    hash_bytes_count: int

    def __init__(self):
        self.messages = []
        self.protocol_name = None
        self.hash_bytes_count = 8

    def parse_meta_section(self, name, items):
        key = items[0]
        value = items[1]
        doc = items[2]

        if name.lower() == "protocol":
            if key == "name":
                print(f"** Define protocol {value}")
                self.protocol_name = value
            if key == "hash_bytes_count":
                print(f"** Hash bytes count = {value}")
                self.hash_bytes_count = int(value)
                # todo: make exception and enum for hash bytes count
                assert(self.hash_bytes_count in [1, 2, 4, 8])

    def declare_message(self, name, items):
        fields = [messages_base.MessageField(_name, _type, _doc) for _name, _type, _doc in items]
        
        # todo: Make new class UserMessage ihnerited from Message
        print(f"Declare {name}")
        user_message = messages_base.Message(name, fields)
        user_message.is_user_defined = True
        self.messages.append(user_message)

    def load(self, data: str):
        current_section = ""
        current_doc_comment = ""
        config = {}

        for line in data.split("\n"):
            line = line.strip()

            if not line:
                continue

            if line[0] == "[" and line[-1] == "]":
                current_section = line[1:-1]
                current_doc_comment = ""
            else:
                if line[0] == ";" or line[0] == "#":
                    current_doc_comment += line[1:] + "\n"
                else:
                    items = list(map(lambda x: x.strip(), line.split("=")))
                    config.setdefault(current_section, []).append((items[0], items[1], current_doc_comment))
                    current_doc_comment = ""

        for section, values in config.items():
            if section[0] == '.':
                for value in values:
                    self.parse_meta_section(section[1:], value)
            else:
                self.declare_message(section, values)

    def load_file(self, filename: str):
        with open(filename, "r") as file:
            self.load(file.read())
