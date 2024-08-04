
from messages.base import Message, MessageField


class MessFilters:
    def __init__(self, jinja_env):
        self.jinja_env = jinja_env

    @classmethod
    def register(cls, env: 'Environment', backend: 'Backend'):
        instance = cls(env)
        filters = {
            'wrap': instance.wrap,
            'field_name': instance.field_name,
            'field_type': instance.field_type,
            'field_message': instance.field_message,
            # 'message': instance.message,
            'message_pure_type': instance.message_pure_type,
            'message_type': instance.message_type,
            'message_var_fields': instance.message_var_fields,
            'message_novar_fields': instance.message_novar_fields,
            'message_docs': instance.message_docs,
        }

        env.filters.update(filters)
        env.globals['backend'] = backend

    def wrap(self, s, a, b) -> str:
        return str(a) + str(s) + str(b)

    def field_name(self, field: MessageField) -> str:
        return field.name

    def field_type(self, field: MessageField) -> str:
        return self.jinja_env.globals['backend'].mangle_message(field.message)

    def field_message(self, field: MessageField) -> Message:
        return field.message
    
    # def message(self, data: dict) -> str:
    #     return data['message']

    def message_pure_type(self, message: Message) -> str:
        return message.name
    
    def message_type(self, message: Message) -> str:
        return self.jinja_env.globals['backend'].mangle_message(message)

    def message_docs(self, message: Message) -> str:
        return message.docs

    def message_var_fields(self, message: Message) -> str:
        return [field for field in message.fields if field.message.is_variative]

    def message_novar_fields(self, message: Message) -> str:
        return [field for field in message.fields if not field.message.is_variative]
