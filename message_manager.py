import typing
from dataclasses import dataclass

from exceptions import CyclicDependencyError, UnresolvedDependencyError
from message import Message
from topo_sort import TopologicalSort


class MessageManager:
    sorter: TopologicalSort
    defined_messages: dict[str, Message]
    sorted_messages: [Message]

    def __init__(self):
        self.sorter = TopologicalSort()
        self.defined_messages = {}
        self.sorted_messages = []

        self._uml = open("test.uml", "w")

    def register(self, message: Message):
        message.link_manager(self)

        self.defined_messages[message.name] = message

        childs = list(map(lambda x: x.message_name, message.fields))

        for child in childs:
            child_generic_name, child_generic_args = self.deserialize_message_name(child)
            if not child_generic_args:
                continue

            self.sorter.add_node(child, [child_generic_name] + child_generic_args)

        self.sorter.add_node(message.name, childs)

    @staticmethod
    def get_serialized_message_name(message: Message):
        return message.get_serialized_message_name()

    @staticmethod
    def deserialize_message_name(type_name):
        # todo: make multiple nested types
        left_bracket = type_name.find('<')
        right_bracket = type_name.rfind('>')

        generic_args = []

        if left_bracket < right_bracket:
            generic_args = list(map(str.strip, type_name[left_bracket + 1:right_bracket].split(",")))
            type_name = type_name[:left_bracket]

        return type_name, generic_args

    def get_all(self):
        return self.sorted_messages

    def get(self, type_name):
        type_name, generic_args = self.deserialize_message_name(type_name)

        message = self.defined_messages.get(type_name, None)
        if not message:
            return None
        if generic_args:
            if not message.generic_args:
                raise RuntimeError(f"Attempt usage simple message {type_name} as generic")
            if len(generic_args) < len(message.generic_args):
                raise RuntimeError(f"Incomplete generic definition: {type_name} with {len(generic_args)} arguments. "
                                   f"({type_name} has {len(message.generic_args)} arguments)")
            if len(generic_args) > len(message.generic_args):
                raise RuntimeError(f"Adjective generic definition: {type_name} with {len(generic_args)} arguments. "
                                   f"({type_name} has {len(message.generic_args)} arguments)")
            message.generic_args = generic_args


        return message

    def get_message(self, type_name):
        msg = self.defined_messages.get(type_name, None)
        if msg is None:
            return None

        return msg.message

    def check_messages_defined(self):
        undefined_list = [rule for rule in self.load_fields_links.keys() if self.get(rule) is None]

        if undefined_list:
            raise UnresolvedDependencyError(", ".join(undefined_list))

    def resolve_dependencies(self):
        self.sorted_messages.clear()

        for node in self.sorter.make_sort()[::-1]:
            if node not in self.defined_messages:
                print(f"Warning: {node}")
                continue

            self.sorted_messages.append(self.defined_messages.get(node))

        self._uml.write("@startuml\n")
        for parent, msg in self.defined_messages.items():
            parent_name = parent.replace('<', '_').replace('>', '_')
            for child in msg.fields:
                child_name = child.message_name.replace('<', '_').replace('>', '_')
                self._uml.write(f"{child_name} <|-- {parent_name}\n")
        self._uml.write("@enduml\n")
