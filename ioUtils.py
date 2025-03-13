import argparse
import os
from Particle import Particle

def parse_arguments(cli_args):
    """ Parses CLI arguments. """
    parser = argparse.ArgumentParser(description="Cell Index Method Simulation")
    parser.add_argument("--static_file", type=str, help="Path to the static input file")
    parser.add_argument("--dynamic_file", type=str, help="Path to the dynamic input file")
    parser.add_argument("--output_file", type=str, help="Path to the output file", default="out1.txt")
    parser.add_argument("--rc", type=float, help="Interaction radius for the Cell Index Method")
    parser.add_argument("--m", type=int, help="Grid dimension for the Cell Index Method", default=0)
    parser.add_argument('--periodic_boundaries', type=lambda x: (str(x).lower() == 'true'), required=True, help='Use periodic boundaries')
    parser.add_argument('--brute_force', type=lambda x: (str(x).lower() == 'true'), required=True, help='Use brute force method')

    return parser.parse_args(cli_args)

def validate_arguments(args):
    """ Validates CLI arguments. """
    if not os.path.exists(args.static_file):
        raise FileNotFoundError(f"File {args.static_file} not found.")
    if not os.path.exists(args.dynamic_file):
        raise FileNotFoundError(f"File {args.dynamic_file} not found.")
    if args.rc <= 0:
        raise ValueError("Cutoff radius must be a positive real number.")
    if args.brute_force == False and args.m <= 0:
        raise ValueError("Grid dimension must be at least 1 to use the Cell Index Method.")
    if args.brute_force:
       args.m = 0

    return args

def parse_input_files(static_file, dynamic_file):
    """ Parses the input files to extract particle data and matrix side length. """
    particles = []
    with open(static_file, 'r') as f_static, open(dynamic_file, 'r') as f_dynamic:
        particle_count = int(f_static.readline().strip())
        matrix_side_length = float(f_static.readline().strip())
        next(f_dynamic)  # Skip the first line of the dynamic file
        for static_line, dynamic_line in zip(f_static, f_dynamic):
            r, p = map(float, static_line.strip().split())  # radius and property
            x, y = map(float, dynamic_line.strip().split())
            particles.append({'x': x, 'y': y, 'radius': r, 'property': p})

    particle_objects = [Particle(p['x'], p['y'], p['radius'], p['property']) for p in particles]

    return {
        'particle_count': particle_count,
        'matrix_side_length': matrix_side_length,
        'particles': particle_objects
    }

def write_output(execution_time, neighbors, output_file):
    """ Writes the output to a file. """
    with open(output_file, 'w') as f:
        f.write(f"{execution_time:.6f}\n")
        for particle, neighbors in neighbors.items():
            f.write(f"{particle}\t{', '.join(map(str, neighbors))}\n")