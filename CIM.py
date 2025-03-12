import math
from collections import OrderedDict
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
        result = OrderedDict((i, set()) for i in range(len(self.particles)))

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
        """ Cell Index Method with fixed boundaries """
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
        self.find_neighbors_cell(grid[row][col], particle_idx, neighbors, result)
        # Check the upper cell
        if row > 0:
            self.find_neighbors_cell(grid[row - 1][col], particle_idx, neighbors, result)
        # Check the lower cell
        if row < self.m - 1:
            self.find_neighbors_cell(grid[row + 1][col], particle_idx, neighbors, result)
        # Check the right cell
        if col < self.m - 1:
            self.find_neighbors_cell(grid[row][col + 1], particle_idx, neighbors, result)
        # Check the diagonal lower-right cell
        if row < self.m - 1 and col < self.m - 1:
            self.find_neighbors_cell(grid[row + 1][col + 1], particle_idx, neighbors, result)

    def find_neighbors_cell(self,
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
        """ Cell Index Method with periodic boundaries """
        for particle_idx, current_particle in enumerate(self.particles):
            i_matrix = self.calculate_cell_idx(current_particle.y)
            j_matrix = self.calculate_cell_idx(current_particle.x)

            neighbors = result.setdefault(particle_idx, set())

            self.find_neighbors_cell(particles_grid[i_matrix][j_matrix], particle_idx, neighbors, result)

            if i_matrix > 0:
                self.find_neighbors_cell(particles_grid[i_matrix - 1][j_matrix], particle_idx, neighbors, result)
            else:
                self.find_neighbors_cell_periodic_downwards(particles_grid[self.m - 1][j_matrix], particle_idx,
                                                            neighbors, result)

            if i_matrix < self.m - 1:
                self.find_neighbors_cell(particles_grid[i_matrix + 1][j_matrix], particle_idx, neighbors, result)
            else:
                self.find_neighbors_cell_periodic_vertical(particles_grid[0][j_matrix], particle_idx, neighbors,
                                                           result)

            if j_matrix < self.m - 1:
                self.find_neighbors_cell(particles_grid[i_matrix][j_matrix + 1], particle_idx, neighbors, result)
            else:
                self.find_neighbors_cell_periodic_horizontal(particles_grid[i_matrix][0], particle_idx,
                                                             neighbors, result)

            if i_matrix < self.m - 1 and j_matrix < self.m - 1:
                self.find_neighbors_cell(particles_grid[i_matrix + 1][j_matrix + 1], particle_idx, neighbors,
                                         result)
            else:
                self.find_neighbors_cell_periodic_diagonal(particles_grid[0][0], particle_idx, neighbors, result)


    ## Distances, and neighbor search with periodic boundaries
    def compute_periodic_distance_downwards(self, target_idx, other_idx):
        # Note we're moving the position of the target particle to the next row of the grid
        target_p = self.particles[target_idx]
        other_p = self.particles[other_idx]
        l = self.l

        return math.sqrt((target_p.x - other_p.x) ** 2 + (target_p.y + l - other_p.y) ** 2)

    def compute_periodic_distance_vertical(self, target_idx, other_idx):
        # Note we're moving the position of the other particle to the next row of the grid
        target_p = self.particles[target_idx]
        other_p = self.particles[other_idx]
        l = self.l

        return math.sqrt((target_p.x - other_p.x) ** 2 + (target_p.y - (other_p.y + l)) ** 2)

    def compute_periodic_distance_horizontal(self, target_idx, other_idx):
        # Note we're moving the position of the other particle to the next col of the grid
        target_p = self.particles[target_idx]
        other_p = self.particles[other_idx]
        l = self.l

        return math.sqrt((target_p.x - (other_p.x + l)) ** 2 + (target_p.y - other_p.y) ** 2)

    def compute_periodic_distance_diagonal(self, target_idx, other_idx):
        # Note we're moving the position of the other particle to the next row and col of the grid
        target_p = self.particles[target_idx]
        other_p = self.particles[other_idx]
        l = self.l

        return math.sqrt((target_p.x - (other_p.x + l)) ** 2 + (target_p.y - (other_p.y + l)) ** 2)

    def is_within_interaction_range(self, distance, radius):
        return (distance - radius <= self.rc) or (distance + radius <= self.rc)

    def find_neighbors_cell_periodic_horizontal(self, cell_particles, target_idx, neighbors, result):
        target_particle = self.particles[target_idx]
        for idx in cell_particles:
            distance = self.compute_periodic_distance_horizontal(target_idx, idx)
            if target_idx != idx and self.is_within_interaction_range(distance, target_particle.radius):
                neighbors.add(idx)
                if idx not in result:
                    result[idx] = set()
                result[idx].add(target_idx)

    def find_neighbors_cell_periodic_vertical(self, cell_particles, target_idx, neighbors, result):
        target_particle = self.particles[target_idx]
        for cell_particle_idx in cell_particles:
            distance = self.compute_periodic_distance_vertical(target_idx, cell_particle_idx)
            if target_idx != cell_particle_idx and self.is_within_interaction_range(distance, target_particle.radius):
                neighbors.add(cell_particle_idx)
                if cell_particle_idx not in result:
                    result[cell_particle_idx] = set()
                result[cell_particle_idx].add(target_idx)

    def find_neighbors_cell_periodic_diagonal(self, cell_particles, target_idx, neighbors, result):
        target_particle = self.particles[target_idx]
        for idx in cell_particles:
            distance = self.compute_periodic_distance_diagonal(target_idx, idx)
            if target_idx != idx and self.is_within_interaction_range(distance, target_particle.radius):
                neighbors.add(idx)
                if idx not in result:
                    result[idx] = set()
                result[idx].add(target_idx)

    def find_neighbors_cell_periodic_downwards(self, cell_particles, target_idx, neighbors, result):
        target_particle = self.particles[target_idx]
        for idx in cell_particles:
            distance = self.compute_periodic_distance_downwards(target_idx, idx)
            if target_idx != idx and self.is_within_interaction_range(distance, target_particle.radius):
                neighbors.add(idx)
                if idx not in result:
                    result[idx] = set()
                result[idx].add(target_idx)