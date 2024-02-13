import argparse

from generator import Generator
from backend import CppBackend

if __name__ == "__main__":
    generator = Generator(CppBackend())

    # parser = argparse.ArgumentParser(description='Optional app description')

    # # Required positional argument
    # parser.add_argument('out', type=str,
    #                     help='Path to generated cpp file')

    # parser.add_argument('in', type=str,
    #                     help='Path to messages')

    # args = vars(parser.parse_args())
    args = {
        'in': 'messages/test.ini',
        'out': 'test.cpp'
    }

    generator.load_file(args["in"])
    generator.write_to_file(args["out"])
