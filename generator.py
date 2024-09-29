import datetime
import hashlib
import typing

from backend import Backend
from exceptions import MessageNotFoundError
from ini_parser import MessageIniParser
from message_manager import MessageManager
import messages.base


class Generator:
    # message_manager: MessageManager
    ini_parser: MessageIniParser
    backend: Backend

    builtin_types: dict[str, messages.base.Message] = {
        "Message": messages.base.Message,
        "Int8": messages.base.Int8,
        "Int16": messages.base.Int16,
        "Int32": messages.base.Int32,
        "Uint8": messages.base.Uint8,
        "Uint16": messages.base.Uint16,
        "Uint32": messages.base.Uint32,
        "Float": messages.base.Float,
        "Fixed16": messages.base.Fixed16,
        "Fixed32": messages.base.Fixed32,
        "VarArray": messages.base.VarArray,
    }

    def __init__(self, backend: Backend):
        self.ini_parser = MessageIniParser()

        self.backend = backend
        self.populate_builtin_types()

    def populate_builtin_types(self):
        for type_name, type_decl in self.builtin_types.items():
            self.backend.register_message(type_decl())

    def load_file(self, filename: str):
        self.ini_parser.load_file(filename)

        for user_message in self.ini_parser.messages:
            self.backend.register_message(user_message)

    def render_message(self, name: str):
        message = self.backend.message_manager.get_message(name)
        if message is None:
            raise MessageNotFoundError(name)
        
        return self.backend.render_message(message)
    
    def hook(self):
        print("Hooked!")

    def write_to_file(self, filename: str):
        self.backend.message_manager.resolve_dependencies()
        print("** Resolved dependencies")

        messages = self.backend.message_manager.get_all()

        
        print(f"** Render protocol")
        with open(filename, "w") as output:
            messages_to_render = []
            wired_count = 0
            for message in messages:
                message_type = self.backend.message_manager.get_serialized_message_name(message)

                if not message.check_definition():
                    raise RuntimeError(f"Invalid definition {message}")
                
                if not message.is_user_defined and (message_type == "Message" or message.is_template and len(message.generic_args) == 0):
                    print(f"-- Skip template {message_type}")
                    continue

                if message.is_user_defined:
                    wired_count += 1

                messages_to_render.append((message.get_render_template(), message))

            render_index = 0
            def hook_on_message_render(msg):
                nonlocal render_index, messages_to_render
                render_index += 1
                cnt = len(messages_to_render)
                dig_cnt = len(str(cnt))
                print(f"[{render_index:0>{dig_cnt}}/{cnt}] Rendered {msg}")
            
            wired_index = 0
            def hook_on_message_usings(msg):
                nonlocal wired_index, wired_count
                wired_index += 1
                dig_cnt = len(str(wired_count))
                print(f"[{wired_index:0>{dig_cnt}}/{wired_count}] Wired {msg}")

            protocol_hash_bytes_count = self.ini_parser.hash_bytes_count
            messages_hash = hashlib.sha256(";".join([str(msg[1]) for msg in messages_to_render]).encode()).digest()
            protocol_hash = int.from_bytes(messages_hash[:protocol_hash_bytes_count], byteorder='little')


            # message_code = self.render_message(str(message))
            output_src = self.backend.get_template("Output.j2").render(data={
                'current_time': str(datetime.datetime.now()),
                'protocol_name': self.ini_parser.protocol_name,
                'protocol_hash_bytes_count': protocol_hash_bytes_count,
                'protocol_hash': protocol_hash,
                'messages': messages_to_render,
                'backend': self.backend,
                'generator': self,
                'hook_on_message_render': hook_on_message_render,
                'hook_on_message_usings': hook_on_message_usings,
            })
            output.write(output_src + "\n")
