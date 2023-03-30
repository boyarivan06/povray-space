from typing import List
from math import sin, cos, pi
from vapory import *
from moviepy.editor import VideoClip
from povray_space import SpaceScene, PlanetSystem, Star, Planet


scene = SpaceScene()
solar_system = PlanetSystem()
other_system = PlanetSystem([20, 5, 20], 10)
trantor = Planet(color=[0, 1, 0])
other_system.add_planet(trantor)
earth = Planet()
mars = Planet(radius=3, star_distance=12, circulation_period=8, color=[1, 0, 0])
venus = Planet(radius=2.5, star_distance=15, circulation_period=13, color=[1, 0, 1])
solar_system.add_planet(earth)
solar_system.add_planet(mars)
solar_system.add_planet(venus)
scene.add_system(solar_system)
scene.add_system(other_system)
# scene.make_gif(duration=20)
scene.make_png(56)
scene.show()
