from math import pi, sin, cos
from typing import List

from space_objects import Star


class PlanetSystem:
    def __init__(self, rotation_center=None, rotation_center_distance=0,
                 star=None, circulation_period=200, angle=0):
        if rotation_center is None:
            rotation_center = [0, 0, 0]
        self.rotation_center = rotation_center
        self.circulation_period = circulation_period
        self.rotation_center_distance = rotation_center_distance

        self.center = [self.rotation_center[0] + sin(angle) * self.rotation_center_distance, self.rotation_center[1],
                       self.rotation_center[2] + cos(angle) * self.rotation_center_distance]
        if star is None:
            star = Star(planet_system=self)
        self.star = star
        '''if planets is None:
            planets = []
        else:
            for n, planet in enumerate(planets):
                planets[n].system_center = self.center
        self.planets = planets'''
        self.planets = []

    def assemble(self, time) -> List:
        angle = pi * time / self.circulation_period
        self.center = [self.rotation_center[0] + sin(angle) * self.rotation_center_distance, self.rotation_center[1],
                       self.rotation_center[2] + cos(angle) * self.rotation_center_distance]
        result = self.star.assemble() + \
            [planet.assemble(time) for planet in self.planets]
        return result

    def add_planet(self, planet):
        self.planets.append(planet)
        planet.system_center = self.center
