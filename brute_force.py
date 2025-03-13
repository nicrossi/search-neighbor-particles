import math as m
from collections import OrderedDict
from typing import List, Set, Dict


class BruteForce:
    def __init__(self, context):
        self.l = context['matrix_side_length']
        self.particles = context['particles']
        self.rc = context['rc']
        self.periodic = context['periodic_boundaries']

    # TODO: periodic boundaries
    def brute_force_method(self) -> Dict[int, Set[int]]:
        # Total number of particles
        number_particles = len(self.particles)

        # Parameter L
        square_side_length = self.l

        # Positions of particles in List
        particles = []
        for i in range(number_particles):
            particles.append((self.particles[i].x, self.particles[i].y))

        # maximum radius of particles
        max_radius = max(p.radius for p in self.particles)
        # property of particles

        # Definition of interaction radius
        radius_interaction = self.rc

        # time steps
        # sample starting line 3, columns 2: particle properties later on

        # Output dictionary
        output_distances = dict()
        result = OrderedDict((i, set()) for i in range(len(self.particles)))

        for p_1 in range(number_particles):
            neighbor_index_list = []
            periodic_particles = []

            if self.periodic:  # TODO: check whether square is a box from 0 to L
                if self.l - particles[p_1][0] <= radius_interaction + 2 * max_radius:
                    periodic_particles.append((particles[p_1][0] - self.l, particles[p_1][1]))

                    if self.l - particles[p_1][1] <= radius_interaction + 2 * max_radius:
                        periodic_particles.append((particles[p_1][0] - self.l, particles[p_1][1] - self.l))
                    if particles[p_1][1] <= 2 * radius_interaction + max_radius:
                        periodic_particles.append((particles[p_1][0] - self.l, particles[p_1][1] + self.l))

                if self.l - particles[p_1][1] <= radius_interaction + 2 * max_radius:
                    periodic_particles.append((particles[p_1][0], particles[p_1][1] - self.l))

                if particles[p_1][0] <= radius_interaction + 2 * max_radius:
                    periodic_particles.append((particles[p_1][0] + self.l, particles[p_1][1]))

                    if self.l - particles[p_1][1] <= radius_interaction + 2 * max_radius:
                        periodic_particles.append((particles[p_1][0] + self.l, particles[p_1][1] - self.l))
                    if particles[p_1][1] <= radius_interaction + 2 * max_radius:
                        periodic_particles.append((particles[p_1][0] + self.l, particles[p_1][1] + self.l))

                if particles[p_1][1] <= radius_interaction + 2 * max_radius:
                    periodic_particles.append((particles[p_1][0], particles[p_1][1] + self.l))

            for p_2 in range(number_particles):
                if p_1 != p_2:  # TODO: check radius correct
                    if m.dist(particles[p_1], particles[p_2]) <= radius_interaction + 2 * max_radius:
                        neighbor_index_list.append(p_2)
                    else:
                        for particle in periodic_particles:
                            if m.dist(particle, particles[p_2]) <= radius_interaction + 2 * max_radius:
                                neighbor_index_list.append(p_2)

            output_distances[p_1] = neighbor_index_list
            for idx in neighbor_index_list:
                result[p_1].add(idx)
        # choose point and visualize with neighbors

        return result
