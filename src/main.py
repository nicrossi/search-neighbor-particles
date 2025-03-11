import sys
import time

from ioUtils import parse_arguments, validate_arguments, parse_input_files
from src.CIM import CIM


def main(args):
    context = generate_context(args)
    cim = CIM(context)

    start_time = time.time()
    neighbors = cim.search_neighbor_particles()
    end_time = time.time()

    duration = end_time - start_time
    print(f"Execution time: {duration:.3f} seconds")

    # TODO implement write output to file


def generate_context(args):
    """ Generates the simulation context from the CLI arguments and input files. """
    cli_args = validate_arguments(parse_arguments(args))
    file_args = parse_input_files(cli_args.static_file, cli_args.dynamic_file)
    context = {**vars(cli_args), **file_args}

    return context


if __name__ == "__main__":
    main(sys.argv[1:])