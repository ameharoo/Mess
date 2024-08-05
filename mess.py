import argparse
import inspect

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

    parser = argparse.ArgumentParser(description="Optional app description")

    # Required positional argument
    parser.add_argument("backend", type=str, help="Backend, one from the list", choices=backends.keys())
    parser.add_argument("out", type=str, help="Path to generated cpp file")

    parser.add_argument("in", type=str, help="Path to messages")

    args = vars(parser.parse_args())

    selected_backend = backends[args["backend"]]()
    generator = Generator(selected_backend)

    generator.load_file(args["in"])
    generator.write_to_file(args["out"])
