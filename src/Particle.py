import math

class Particle:
    def __init__(self, x, y, radius, property):
        """ Instance particle with its pasition, radius and properties """
        self.x = x
        self.y = y
        self.radius = radius
        self.property = property

    def distance_to(self, other_particle):
        """ Calculates the distance to another particle. """
        dx = self.x - other_particle.x
        dy = self.y - other_particle.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_radius(self):
        return self.radius

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_radius(self, radius):
        self.radius = radius

    def get_property(self):
        return self.property

    def set_property(self, property):
        self.property = property

    def __repr__(self):
        return f"Particle(x={self.x}, y={self.y}, radius={self.radius}, property={self.property})"