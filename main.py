from typing import List
from math import sin, cos, pi
from vapory import *
from moviepy.editor import VideoClip
from povray_space import SpaceScene, PlanetSystem, Star, Planet


scene = SpaceScene()
solar_system = PlanetSystem()
earth = Planet()
mars = Planet(radius=3, star_distance=12, circulation_period=8, color=[1, 0, 0])
solar_system.add_planet(earth)
solar_system.add_planet(mars)
scene.add_system(solar_system)
scene.make_gif(duration=20)
