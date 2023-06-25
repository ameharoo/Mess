import typing

from message import TypeField, CppType
from message_manager import global_message_manager


class MessageIniParser:
    load_fields_links: dict[str, list[typing.Type]]

    def __init__(self):
        self.load_fields_links = {}

    def parse_meta_section(self, name, items):
        key = items[0]
        value = items[1]
        doc = items[2]

        if name.lower() == "protocol":
            if key == "name":
                print(f"** Define protocol {value}")

    def declare_message(self, name, items):
        fields = [TypeField(_type, _name, _doc) for _name, _type, _doc in items]

        cls = type(name, (CppType,), {
            "render_type_name": lambda self: name,
            "load_fields": fields,
            "field_count": len(fields)
        })

        for field in fields:
            for arg in field.fetch_types():
                self.load_fields_links.setdefault(arg, []).append(cls)

        print(f"Declare {name}")

        global_message_manager.register(name, cls)
        self.load_fields_links.setdefault(name, [])

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
