import typing
import dataclasses

@dataclasses.dataclass()
class ParsedMessageField():
    name: str
    type: str
    docs: str

@dataclasses.dataclass()
class ParsedMessage():
    name: str
    fields: []
    docs: str

class MessageIniParser:
    messages: [ParsedMessage]

    def __init__(self,):
        self.messages = []

    def parse_meta_section(self, name, items):
        key = items[0]
        value = items[1]
        doc = items[2]

        if name.lower() == "protocol":
            if key == "name":
                # todo: namespaces
                print(f"** Define protocol {value}")

    def declare_message(self, name, items):
        print(f"Declare {name}")
        fields = [ParsedMessageField(name, type_, docs) for name, type_, docs in items]
        self.messages.append(ParsedMessage(name, fields, "")) # todo: make docs for message

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
