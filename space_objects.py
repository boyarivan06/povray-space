from math import pi, sin, cos
from typing import Any, List

from vapory import Texture, Pigment, Sphere, LightSource


class Planet:
    def __init__(self, radius=1, star_distance=15, color=None, planet_system: Any = None, circulation_period=10):

        if planet_system is None:
            raise TypeError
        else:
            planet_system.add_planet(self)
            self.system = planet_system

        if color is None:
            self.texture = Texture(Pigment('color', [1, 1, 1]))
        else:
            self.texture = Texture(Pigment('color', color))
        self.radius = radius
        self.star_distance = star_distance
        self.circulation_period = circulation_period

    def assemble(self, time) -> Sphere:
        angle = pi * time / self.circulation_period
        return Sphere([self.system.center[0] + sin(angle) * self.star_distance, self.system.center[1],
                       self.system.center[2] + cos(angle) * self.star_distance], self.radius, self.texture)


class Star:
    def __init__(self, radius=3, color=None, planet_system=None):
        if planet_system is None:
            raise TypeError
        else:
            self.system = planet_system
        if color is None:
            self.texture = Texture(Pigment('color', [1, 1, 0, .0]))
        else:
            self.texture = Texture(Pigment('color', color))
        self.radius = radius

    def assemble(self) -> List:
        return [Sphere(self.system.center, self.radius, self.texture),
                LightSource(self.system.center, 'color', [1, 1, 1])]
