import typing
from dataclasses import dataclass

from exceptions import CyclicDependencyError, UnresolvedDependencyError
from topo_sort import TopologicalSort

import messages.base as messages_base


class MessageManager:
    sorter: TopologicalSort
    defined_messages: dict[str, messages_base.Message]
    sorted_messages: list[messages_base.Message]

    def __init__(self):
        self.sorter = TopologicalSort()
        self.defined_messages = {}
        self.sorted_messages = []

    def register(self, message: messages_base.Message):
        assert(not message.name[0].isnumeric())
        
        self.defined_messages[message.get_serialized_message_name()] = message

        # print(self.defined_messages)

        childs = list(map(lambda x: x.message_name, message.fields))

        for child in childs:
            self.register_message_name(child)
        self.sorter.add_node(message.name, childs)

        print(f"* Registered {message.name}" + "".join([f"\n-- {child}" for child in childs]))

    def register_message_name(self, name: str):
        child_generic_name, child_generic_args = self.deserialize_message_name(name)
        if not child_generic_args:
            return
        
        # Attempt retrieve variadic message and fill
        orig_message = self.get(child_generic_name)
        assert(orig_message is not None)
        var_message = type(orig_message)() # todo: fix different init signatures
        # var_message.name = name
        var_message.generic_args = [messages_base.GenericArg(arg) for arg in child_generic_args]
        
        self.defined_messages[name] = var_message
        
        self.sorter.add_node(name, child_generic_args)
        print(f"-- Registered nested {name}")
        
        for child in child_generic_args:
            self.register_message_name(child)


    @staticmethod
    def get_serialized_message_name(message: messages_base.Message):
        return message.get_serialized_message_name()

    @staticmethod
    def deserialize_message_name(type_name):
        # todo: make multiple nested types
        left_bracket = type_name.find('<')
        right_bracket = type_name.rfind('>')

        generic_args = []

        if left_bracket < right_bracket:
            generic_args = list(map(str.strip, type_name[left_bracket+1:right_bracket].split(",")))
            type_name = type_name[:left_bracket]

        return type_name, generic_args

    def get_all(self) -> list[messages_base.Message]:
        return self.sorted_messages

    def get(self, type_name) -> messages_base.Message:
        type_name, generic_args = self.deserialize_message_name(type_name)

        message = self.defined_messages.get(type_name, None)
        
        assert(message is not None)
        if not message:
            return None

        return message

    def get_message(self, type_name) -> messages_base.Message:
        msg = self.defined_messages.get(type_name, None)
        if msg is None:
            return None

        return msg
        
    def make_fields_init(self, message: messages_base.Message):
        for field in message.fields:
            field.message = self.get_message(field.message_name)
            assert(field.message is not None)

        for arg in message.generic_args:
            arg.message = self.get_message(arg.name)
            assert(arg.message is not None)

    def resolve_dependencies(self):
        self.sorted_messages.clear()

        for node in self.sorter.make_sort()[::-1]:
            if node not in self.defined_messages:
                print(f"Warning: {node}")
                continue

            msg = self.get_message(node)

            self.sorted_messages.append(msg)

            self.make_fields_init(msg)

