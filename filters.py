from message import MessageField, Message


class MessFilters:
    @classmethod
    def register(cls, env: 'Environment'):
        filters = {
            'wrap': cls.wrap,
            'field_name': cls.field_name,
            'field_type': cls.field_type,
            'field_message': cls.field_message,
            'message_type': cls.message_type,
            'message_var_fields': cls.message_var_fields,
            'message_novar_fields': cls.message_novar_fields,
            'message_docs': cls.message_docs,
        }

        env.filters.update(filters)

    @staticmethod
    def wrap(s, a, b) -> str:
        return str(a) + str(s) + str(b)

    @staticmethod
    def field_name(field: MessageField) -> str:
        return field.name

    @staticmethod
    def field_type(field: MessageField) -> str:
        return field.message.name

    @staticmethod
    def field_message(field: MessageField) -> Message:
        return field.message

    @staticmethod
    def message_type(message: Message) -> str:
        return message.name

    @staticmethod
    def message_docs(message: Message) -> str:
        return message.docs

    @staticmethod
    def message_var_fields(message: Message) -> str:
        return [field for field in message.fields if field.message.is_variative]

    @staticmethod
    def message_novar_fields(message: Message) -> str:
        return [field for field in message.fields if not field.message.is_variative]
