import argparse
import inspect
import os
import pkgutil
from typing import Callable

from jinja2 import Environment, PackageLoader, select_autoescape

from filters import MessFilters
from message_manager import MessageManager

import messages
import messages.base as messages_base


class Backend:
    message_manager: MessageManager
    implementations: dict[str, messages_base.Message]
    name: str
    path_to_templates: str
    builtin_messages: [str]

    def __init__(self):
        self.message_manager = MessageManager()
        self.jinja_env = Environment(
            loader=PackageLoader("backend", "templates/"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True,
            extensions=['jinja2.ext.do', 'jinja2.ext.loopcontrols']
        )

        MessFilters.register(self.jinja_env, self)

        self.register_implementations()

    def get_arguments() -> argparse.ArgumentParser:
        return argparse.ArgumentParser(add_help=False)
    
    def process_arguments(self, args=dict[str, str]):
        pass

    def register_implementations(self):
        self.implementations = self.get_implementations()

    def register_message(self, message: messages_base.Message):
        dst_impl = self.implementations.get(message.__class__.__name__, None)
        if dst_impl is not None:
            dst_impl = dst_impl()
            dst_impl.name = message.name
            dst_impl.fields = message.fields
            dst_impl.generic_args = message.generic_args
            dst_impl.docs = message.docs
            dst_impl.is_user_defined = message.is_user_defined
        else:
            dst_impl = message

        self.message_manager.register(dst_impl)

    def get_template(self, path: str) -> 'Template':
        return self.jinja_env.get_template(os.path.join(self.path_to_templates, path))

    def render_message(self, message:  messages_base.Message):
        if message.name in self.builtin_messages or message.name == 'Message':
            return None

        return message.render(self)
    
    @classmethod
    def get_implementations(cls):
        implementations = {}
        for importer, modname, ispkg in pkgutil.iter_modules(messages.__path__):
            module = __import__('messages.' + modname, fromlist="dummy")

            if modname == 'base' or modname != cls.name:
                continue

            print(f"* Imported {module.__name__}")
            for name, klass in inspect.getmembers(module):
                if inspect.isclass(klass):
                    implementations[name] = klass
                    print(f"-- Added implementation {module.__name__}.{klass.__qualname__}")
        return implementations
    
    @classmethod
    def mangle_part(cls, type: str, value: str):
        if type == 'T' or type == 'N':
            return f"{type}{len(value)}{value}"
        if type == 'A':
            return f"{type}{value}"
        assert(None)

    @classmethod
    def mangle_message_parts(cls, message:  messages_base.Message):
        parts = [
            cls.mangle_part('T' if len(message.generic_args) > 0 else 'N', message.name)
        ]

        if len(message.generic_args) > 0:
            parts.append(cls.mangle_part('A', len(message.generic_args)))

        for arg in message.generic_args:
            parts += cls.mangle_message_parts(arg.message)

        return parts
    
    @classmethod
    def mangle_message(cls, message:  messages_base.Message):
        return "".join(cls.mangle_message_parts(message))


class CppBackend(Backend):
    name = "cpp"
    path_to_templates = "cpp/"
    builtin_messages = ["Int8", "Int16", "Int32", "Int64"]
    use_highlevel_api = False

    @classmethod
    def get_arguments(cls) -> argparse.ArgumentParser:
        parser = super().get_arguments()
        parser.add_argument('-hl', '--highlevel-api', help="Enable highlevel API", action='store_true')
        return parser

    def process_arguments(self, args):
        self.use_highlevel_api = args['highlevel_api']

    def render_message(self, message:  messages_base.Message):
        return super().render_message(message)

class ImHexBackend(Backend):
    name = "imhex"
    path_to_templates = "imhex/"
    
    def render_message(self, message:  messages_base.Message):
        return super().render_message(message)

class PythonBackend(Backend):
    name = "python"
    path_to_templates = "python/"
    
    def render_message(self, message:  messages_base.Message):
        return super().render_message(message)
