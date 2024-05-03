import typing

from backend import Backend
from exceptions import MessageNotFoundError
import message
from ini_parser import MessageIniParser
from message_manager import MessageManager


class Generator:
    message_manager: MessageManager
    ini_parser: MessageIniParser
    backend: Backend
    # load_fields_links: dict[str, list[typing.Type]]
    # sorted_messages: list[message.Message]

    builtin_types: dict[str, typing.Type] = {
        "Int8": message.Int8(),
        "Int16": message.Int16(),
        # "Int32": message.Int32,
        # "Float": message.Float,
        # "Fixed16": message.Fixed16,
        # "Fixed32": message.Fixed32,
        # "VarArray": message.VarArray,
    }

    def __init__(self, backend: Backend):
        self.message_manager = MessageManager()
        self.populate_builtin_types()

        self.ini_parser = MessageIniParser(self)

        self.backend = backend

    def populate_builtin_types(self):
        for type_name, type_decl in self.builtin_types.items():
            self.message_manager.register(type_decl)

    def load_file(self, filename: str):
        self.ini_parser.load_file(filename)

    def render_message(self, name: str):
        message = self.message_manager.get(name)
        if message is None:
            raise MessageNotFoundError(name)
        
        return self.backend.render_message(message)

    def write_to_file(self, filename: str):
        self.message_manager.resolve_dependencies()
        # self.check_types()
        # self.resolve_dependencies()

        print(self.message_manager.get_all())

        print(f"** Render protocol")
        with open(filename, "w") as output:
            for message in self.message_manager.get_all():
                message_code = self.render_message(message.name)
                if message_code:
                    print(f"Successfully rendered {message.name}")
                    output.write(message_code + "\n")

    # def check_types(self):
    #     undefined_list = [rule for rule in self.load_fields_links.keys() if self.message_manager.get(rule) is None]

    #     if undefined_list:
    #         raise UnresolvedDependencyError(", ".join(undefined_list))

    # def resolve_dependencies(self):
    #     self.sorted_messages.clear()

    #     while self.load_fields_links:
    #         gen_list = [rule for rule in self.load_fields_links.keys() if
    #                     self.message_manager.get(rule).field_count == 0]

    #         if not gen_list:
    #             exception_text = ", ".join(
    #                 [rule for rule in self.load_fields_links.keys() if
    #                  self.message_manager.get(rule).field_count != 0])

    #             raise CyclicDependencyError(exception_text)

    #         for rule in gen_list:
    #             self.sorted_messages.append(self.message_manager.get(rule))

    #             for referenced_rule in self.load_fields_links[rule]:
    #                 referenced_rule.field_count -= 1

    #             self.load_fields_links.pop(rule)
