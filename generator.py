import typing

from ini_parser import MessageIniParser
from message import CppType
from message_manager import global_message_manager


class CyclicDependencyError(RuntimeError):
    pass


class Generator:
    ini_parser: MessageIniParser
    load_fields_links: dict[str, list[typing.Type]]
    sorted_messages: list[typing.Type]

    def __init__(self):
        self.load_fields_links = {}
        self.ini_parser = MessageIniParser()
        self.sorted_messages = []

    def load_file(self, filename: str):
        self.ini_parser.load_file(filename)
        self.load_fields_links = self.ini_parser.load_fields_links

    @staticmethod
    def render_message(cls: typing.Type):
        obj: CppType = cls(None)
        if obj.is_builtin:
            return None

        for field in obj.load_fields:
            obj.fields.append(field.instantiate())

        return obj.render_definition()

    def write_to_file(self, filename: str):
        self.resolve_dependencies()

        print(f"** Render protocol")
        with open(filename, "w") as output:
            output.write(open("templates/vararray.cpp", "r").read())

            for message_type in self.sorted_messages:
                message_code = self.render_message(message_type)
                if message_code:
                    print(f"Successfully rendered {message_type.__name__}")
                    output.write(message_code + "\n")

    def resolve_dependencies(self):
        self.sorted_messages.clear()

        while self.load_fields_links:
            gen_list = [rule for rule in self.load_fields_links.keys() if
                        global_message_manager.get(rule).field_count == 0]

            if not gen_list:
                exception_text = ", ".join(
                    [rule for rule in self.load_fields_links.keys() if
                     global_message_manager.get(rule).field_count != 0])
                raise CyclicDependencyError(exception_text)

            for rule in gen_list:
                self.sorted_messages.append(global_message_manager.get(rule))

                for referenced_rule in self.load_fields_links[rule]:
                    referenced_rule.field_count -= 1

                self.load_fields_links.pop(rule)
