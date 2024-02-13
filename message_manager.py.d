import typing
from dataclasses import dataclass

from exceptions import CyclicDependencyError, UnresolvedDependencyError
from message import Message


@dataclass
class MessageWrapper:
    message: Message
    field_count: int = 0


class MessageManager:
    defined_messages: dict[str, MessageWrapper]
    load_fields_links: dict[str, list[MessageWrapper]]
    sorted_messages: dict[str, Message]

    def __init__(self):
        self.defined_messages = {}
        self.load_fields_links = {}
        self.sorted_messages = {}

    def register(self, message: Message):
        wrapper = MessageWrapper(message)

        generic_args_count = 0
        for field in message.fields:
            # Add links to generic argument types
            _, generic_args = self.deserialize_message_name(field.message_name)

            generic_args_count += len(generic_args)

            for generic_arg in generic_args:
                self.load_fields_links.setdefault(generic_arg, []).append(wrapper)

            # Add link to field
            self.load_fields_links.setdefault(field.message_name, []).append(wrapper)

        self.load_fields_links.setdefault(message.name, [])
        wrapper.field_count = len(message.fields) + generic_args_count

        self.defined_messages[message.name] = wrapper

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
            generic_args = list(map(str.strip, type_name[left_bracket+1:right_bracket].split(",")))
            type_name = type_name[:left_bracket]

        return type_name, generic_args

    def get_all(self):
        return self.sorted_messages

    def get(self, type_name):
        type_name, generic_args = self.deserialize_message_name(type_name)

        message = self.defined_messages.get(type_name, None)
        if not message:
            return None

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
        self.check_messages_defined()

        self.sorted_messages.clear()

        while self.load_fields_links:
            gen_list = [rule for rule in self.load_fields_links.keys() if
                        self.get(rule).field_count == 0]

            if not gen_list:
                exception_text = ", ".join(
                    [rule for rule in self.load_fields_links.keys() if
                     self.get(rule).field_count != 0])

                raise CyclicDependencyError(exception_text)

            for rule in gen_list:
                type_name, generic_args = self.deserialize_message_name(rule)

                base_message = self.get(rule)
                if generic_args:
                    new_message = base_message.message.__copy__()
                    new_message.generic_args = generic_args
                else:
                    new_message = base_message.message

                if not (base_message.message.generic_args and not generic_args):
                    self.sorted_messages[rule] = new_message

                for referenced_rule in self.load_fields_links[rule]:
                    referenced_rule.field_count -= 1

                self.load_fields_links.pop(rule)
