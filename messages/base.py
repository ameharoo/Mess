import typing
from dataclasses import dataclass


@dataclass
class MessageField:
    name: str
    message_name: str
    docs: str
    message: typing.Optional['Message'] = None

    def get_message(self) -> 'Message':
        pass

@dataclass
class GenericArg:
    name: str
    message: typing.Optional['Message'] = None


class Message:
    name: str
    fields: list[MessageField]
    generic_args: list[GenericArg]
    is_variative: bool = False
    is_user_defined: bool = False
    is_template: bool = False
    docs: str = ""

    def __init__(self, name=None, fields=None, generic_args=None, docs=None):
        if name is None:
            name = "Message"

        if fields is None:
            fields = []

        if generic_args is None:
            generic_args = []

        if docs is None:
            docs = ""

        self.name = name
        self.fields = fields
        self.generic_args = generic_args
        self.docs = docs

    def __copy__(self):
        return type(self)(self.name, self.fields, self.generic_args)

    def get_serialized_message_name(self):
        if self.generic_args:
            return f"{self.name}<{', '.join([arg.message.get_serialized_message_name() for arg in self.generic_args])}>"
        else:
            return f"{self.name}"

    def get_representable_str(self) -> str:
        return f"{self.get_serialized_message_name()}(" + ",".join([field.message_name for field in self.fields]) + ")"
    
    def __str__(self):
        return self.get_representable_str()

    def do(self):
        print("I base!")

    def render(self, backend: 'Backend') -> str:
        raise NotImplementedError(f"render for {self.__class__.__name__} not implemented for {backend.name} Backend")

    def get_render_template(self) -> str:
        raise NotImplementedError(f"get_render_template for {self.__class__.__name__}")

    def check_definition(self) -> bool:
        return True
    

class Int8(Message):
    name = "Int8"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)


class Int16(Message):
    name = "Int16"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)


class Int32(Message):
    name = "Int32"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)

class Uint8(Message):
    name = "Uint8"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)


class Uint16(Message):
    name = "Uint16"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)


class Uint32(Message):
    name = "Uint32"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)


class Float(Message):
    name = "Float"

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)

class Fixed16(Message):
    name = "Fixed16"
    bitness = 16

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name)

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)

class Fixed32(Message):
    name = "Fixed32"
    bitness = 32

    def __init__(self, name = None):
        if name is None:
            name = self.name
        
        super().__init__(name)

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)

class VarArray(Message):
    name = "VarArray"
    is_variative = True
    is_template = True
    
    def __init__(self, name = None):
        if name is None:
            name = self.name
            
        super().__init__(self.name, [])

    # def render(self, backend: 'Backend') -> str:
    #     raise NotImplementedError(self)

