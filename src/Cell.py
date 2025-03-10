class Cell:
    """
    Represents a cell in the Cell Index Method, containing a set of particle IDs.
    """
    def __init__(self):
        """ Initializes an empty cell. """
        self.particles = set()

    def add_particle(self, particle_id):
        """ Adds a particle ID to the cell. """
        self.particles.add(particle_id)

    def get_particles(self):
        """ Returns the set of particle IDs in the cell. """
        return self.particles

    def __repr__(self):
        return f"Cell(particles={self.particles})"