import dataclasses

import message
from backend import CppBackend
from message_manager import MessageManager
from ini_parser import *

parser = MessageIniParser()
parser.load_file("messages/test.ini")
exit()

backend = CppBackend()

manager = MessageManager()

manager.register(message.Int8())
manager.register(message.Int16())

VarArray = message.Message("VarArray", [
    message.MessageField("length", "Int16"),
], ["T"])
manager.register(VarArray)

A = message.Message("A", [
    message.MessageField("r", "Int8"),
])

B = message.Message("B", [
    message.MessageField("c", "A"),
])

C = message.Message("C", [
    message.MessageField("d", "D"),
])

D = message.Message("D", [
    message.MessageField("c", "A"),
    message.MessageField("b", "B"),
])

Color = message.Message("Color", [
    message.MessageField("r", "Int8"),
    message.MessageField("g", "Int8"),
    message.MessageField("b", "Int8"),
])

LedColor = message.Message("LedColor", [
    message.MessageField("data", "VarArray<Color>"),
])

smth = message.Message("Something", [
    message.MessageField("data", "VarArray<C>"),
])

manager.register(A)
manager.register(B)
manager.register(C)
manager.register(D)

manager.register(LedColor)
manager.register(Color)
manager.register(smth)

manager.resolve_dependencies()

print(backend.render_message(manager.get("Int8")))

#print("\n".join(map(str, manager.get_all())))
