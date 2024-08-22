from messages import base


class Message(base.Message):
    def __init__(self, name=None, fields=None, generic_args=None, docs=None):
        super().__init__(name, fields, generic_args, docs)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "Type.j2"


class Int8(base.Int8):
    name = "Int8"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"


class Int16(base.Int16):
    name = "Int16"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"
    

class Int32(base.Int32):
    name = "Int32"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"
    

class Uint8(base.Uint8):
    name = "Uint8"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"
    

class Uint16(base.Uint16):
    name = "Uint16"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"
    

class Uint32(base.Uint32):
    name = "Uint32"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "UniformInt.j2"
    

class Float(base.Float):
    name = "Float"

    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "Float.j2"
    

class Fixed16(base.Fixed16):
    name = "Fixed16"

    def __init__(self):
        super().__init__()

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "Fixed.j2"
    
  
class Fixed32(base.Fixed32):
    name = "Fixed32"

    def __init__(self):
        super().__init__()

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "Fixed.j2"
    

class VarArray(base.VarArray):
    name = "VarArray"
    is_variative = True
    
    def __init__(self):
        super().__init__(self.name)

    def render(self, backend: 'Backend'):
        return backend.get_template(self.get_render_template()) \
                      .render(data={'message': self, 'backend': backend})
    
    def get_render_template(self) -> str:
        return "VarArray.j2"
    
