import argparse
import inspect
import sys

from generator import Generator     
import backend

if __name__ == "__main__":
    # Search all defined backends
    backends = {}
    for name, klass in inspect.getmembers(backend):
        if inspect.isclass(klass):
            if not issubclass(klass, backend.Backend) or klass == backend.Backend:
                continue
            backends[klass.name] = klass

    # Trick for add backend specific arguments
    parser_parents = []
    if len(sys.argv) > 1:
        cur_backend = backends.get(sys.argv[1], None)
        if cur_backend is not None:
            parser_parents.append(cur_backend.get_arguments())

    parser = argparse.ArgumentParser(description="Optional app description", parents=parser_parents)

    # Required positional argument
    parser.add_argument("backend", type=str, help="Backend, one from the list", choices=backends.keys())
    parser.add_argument("out", type=str, help="Path to generated cpp file")

    parser.add_argument("in", type=str, help="Path to messages")

    args = vars(parser.parse_args())

    selected_backend = backends[args["backend"]]()
    selected_backend.process_arguments(args)

    generator = Generator(selected_backend)
    generator.load_file(args["in"])
    generator.write_to_file(args["out"])
