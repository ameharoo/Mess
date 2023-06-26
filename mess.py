import argparse

from generator import Generator
from message import Int8, Int16, Int32, Float, VarArray, Fixed16, Fixed32
from message_manager import global_message_manager

global_message_manager.register("Int8", Int8)
global_message_manager.register("Int16", Int16)
global_message_manager.register("Int32", Int32)
global_message_manager.register("Float", Float)
global_message_manager.register("Fixed16", Fixed16)
global_message_manager.register("Fixed32", Fixed32)
global_message_manager.register("VarArray", VarArray)

generator = Generator()

parser = argparse.ArgumentParser(description='Optional app description')

# Required positional argument
parser.add_argument('out', type=str,
                    help='Path to generated cpp file')

parser.add_argument('in', type=str,
                    help='Path to messages')

args = vars(parser.parse_args())

generator.load_file(args["in"])
generator.write_to_file(args["out"])
