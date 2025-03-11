import math
from collections import defaultdict
from typing import List, Set, Dict


class CIM:
    def __init__(self, context):
        self.l = context['matrix_side_length']
        self.particles = context['particles']
        self.rc = context['rc']
        self.periodic = context['periodic_boundaries']
        self.m = self.calculate_m(context['m'])

    def search_neighbor_particles(self) -> Dict[int, Set[int]]:
        """ Compute the neighbors of each particle using the Cell Index Method """
        particles_grid = self.populate_grid()
        result = defaultdict(set)

        # TODO implement periodic boundaries "
        if self.periodic:
            self.cim_periodic_boundaries(result, particles_grid)
        else:
            self.cim_fixed_boundaries(result, particles_grid)

        return result

    def calculate_m(self, matrix_size: int) -> int:
        """
        Calculates a suitable grid size (m) for the Cell Index Method based on
        the size of the simulation area (l), the interaction radius (r), and
        the maximum particle radius (max_radius).
        It also validates user-provided grid sizes to ensure compatibility with the simulation parameters
        """
        max_radius = max(p.radius for p in self.particles)
        max_m = math.floor(self.l / (self.rc + 2 * max_radius))
        while self.l / max_m <= 2 * max_radius + self.rc:
            max_m -= 1

        if matrix_size == 0:
            m = max_m
        elif matrix_size > max_m:
            raise ValueError("Selected m size is not compatible with particle radius and r_c")
        else:
            m = matrix_size

        # print(f"Using matrix size (m): {m}")
        return m

    def calculate_cell_idx(self, pos: float) -> int:
        """ Determines the index of a cell in a grid based on a given position """
        return min(self.m - 1, int((pos * self.m) / self.l))

    def populate_grid(self) -> List[List[Set[int]]]:
        """ Initialize and populate the grid with the particles """
        grid = [[set() for _ in range(self.m)] for _ in range(self.m)]
        for i, particle in enumerate(self.particles):
            x_idx = self.calculate_cell_idx(particle.x)
            y_idx = self.calculate_cell_idx(particle.y)
            grid[y_idx][x_idx].add(i)

        return grid

    def cim_fixed_boundaries(self, result: Dict[int, Set[int]], grid: List[List[Set[int]]]):
        for particle_idx, particle in enumerate(self.particles):
            i, j = self.calculate_cell_idx(particle.y), self.calculate_cell_idx(particle.x)
            neighbor_list = result[particle_idx]

            self.check_neighbor_cells(grid, i, j, particle_idx, neighbor_list, result)

    def check_neighbor_cells(self,
                             grid: List[List[Set[int]]],
                             row: int, col: int, particle_idx: int,
                             neighbors: Set[int],
                             result: Dict[int, Set[int]]):
        """ Checks and processes neighboring cells for a given particle in a grid. """
        # Check the current cell
        self.find_neighbor_cells(grid[row][col], particle_idx, neighbors, result)
        # Check the upper cell
        if row > 0:
            self.find_neighbor_cells(grid[row - 1][col], particle_idx, neighbors, result)
        # Check the lower cell
        if row < self.m - 1:
            self.find_neighbor_cells(grid[row + 1][col], particle_idx, neighbors, result)
        # Check the right cell
        if col < self.m - 1:
            self.find_neighbor_cells(grid[row][col + 1], particle_idx, neighbors, result)
        # Check the diagonal lower-right cell
        if row < self.m - 1 and col < self.m - 1:
            self.find_neighbor_cells(grid[row + 1][col + 1], particle_idx, neighbors, result)

    def find_neighbor_cells(self,
                            cell_particles: Set[int],
                            target_idx: int,
                            neighbors: Set[int],
                            result: Dict[int, Set[int]]):
        """
        Identifies neighboring particles within a given cell.
        Parameters:
            cell_particles (Set[int]): Set of particle indices in the current cell.
            target_idx (int): Index of the particle for which neighbors are being found.
            neighbors (Set[int]): Set to store neighboring particle indices.
            result (Dict[int, Set[int]]): Dictionary storing neighbor relationships.
        """
        target_particle = self.particles[target_idx]
        for idx in cell_particles:
            if target_idx == idx: continue  # Skip self-comparison

            distance = target_particle.distance_to(self.particles[idx])

            # Check if within interaction range
            if distance <= self.rc + target_particle.radius:
                neighbors.add(idx)
                result[idx].add(target_idx)

    def cim_periodic_boundaries(self, result, particles_grid):
        pass
        # TODO implement
