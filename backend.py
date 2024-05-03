import os
from typing import Callable

from jinja2 import Environment, PackageLoader, select_autoescape

from filters import MessFilters
from message import Message, MessageField


class Backend:
    name: str
    path_to_templates: str
    builtin_messages: [str]

    def __init__(self):
        self.jinja_env = Environment(
            loader=PackageLoader("backend", "templates/"),
            autoescape=select_autoescape(),
            trim_blocks=True,
            lstrip_blocks=True
        )

        MessFilters.register(self.jinja_env)

    def get_template(self, path: str) -> 'Template':
        return self.jinja_env.get_template(os.path.join(self.path_to_templates, path))

    def render_message(self, message: Message):
        if message.name in self.builtin_messages:
            return None

        return message.render(self)


class CppBackend(Backend):
    name = "cpp"
    path_to_templates = "cpp/"
    builtin_messages = ["Int8", "Int16", "Int32", "Int64"]

    def render_message(self, message: Message):
        if message.name == "Int8":
            return f"using Int8 = std::int8_t;"
        if message.name == "Int16":
            return f"using Int16 = std::int16_t;"
        if message.name == "Int32":
            return f"using Int32 = std::int32_t;"
        if message.name == "Int64":
            return f"using Int64 = std::int64_t;"

        return super().render_message(message)
