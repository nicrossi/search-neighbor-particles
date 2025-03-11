import random
import argparse

def generate_static_input(filename, N, L, radius=None, min_radius=0.0, max_radius=0.5):
    """Generates a text file with N particles in a simulation area of side L."""
    with open(filename, 'w') as f:
        f.write(f"{N}\n")
        f.write(f"{L}\n")

        for _ in range(N):
            particle_radius = radius if radius is not None else round(random.uniform(min_radius, max_radius), 2)
            property_value = 1.0  # not using this value yet, but I'll leave it as placeholder
            f.write(f"{particle_radius} {property_value}\n")


def generate_dynamic_input(filename, N, L, t0=0.0):
    with open(filename, "w") as file:
        file.write(f"{t0}\n")

        for _ in range(N):
            x = random.uniform(0, L)
            y = random.uniform(0, L)
            file.write(f"{x:.1f} {y:.1f}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate particle input files.")
    parser.add_argument("--N", type=int, help="Number of particles")
    parser.add_argument("--L", type=float, help="Side length of the simulation area")
    parser.add_argument("--radius", type=float, default=None, help="Radius of the particles (optional)")
    parser.add_argument("--min_radius", type=float, default=0.0, help="Minimum radius of the particles (optional)")
    parser.add_argument("--max_radius", type=float, default=0.5, help="Maximum radius of the particles (optional)")

    args = parser.parse_args()

    STATIC_INPUT_FILENAME = "particles_static.txt"
    DYNAMIC_INPUT_FILENAME = "particles_dynamic.txt"
    # generate_static_input(STATIC_INPUT_FILENAME, N=args.N, L=args.L, radius=args.radius, min_radius=args.min_radius, max_radius=args.max_radius)
    generate_static_input(STATIC_INPUT_FILENAME, N=args.N, L=args.L, radius=args.radius)
    generate_dynamic_input(DYNAMIC_INPUT_FILENAME, N=args.N, L=args.L)