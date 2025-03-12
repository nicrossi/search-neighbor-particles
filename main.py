import sys
import time

from brute_force import BruteForce
from ioUtils import parse_arguments, validate_arguments, parse_input_files, write_output
from CIM import CIM


def main(args):
    context = generate_context(args)
    cim = CIM(context)
    bf = BruteForce(context)

    start_time = time.time()
    if context['brute_force']:
        neighbors = bf.brute_force_method()
    else:
        neighbors = cim.search_neighbor_particles()
    end_time = time.time()

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.3f} seconds")

    write_output(execution_time, neighbors, context['output_file'])


def generate_context(args):
    """ Generates the simulation context from the CLI arguments and input files. """
    cli_args = validate_arguments(parse_arguments(args))
    file_args = parse_input_files(cli_args.static_file, cli_args.dynamic_file)
    context = {**vars(cli_args), **file_args}

    return context


if __name__ == "__main__":
    main(sys.argv[1:])