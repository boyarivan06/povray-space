from typing import List
from math import sin, cos, pi
from vapory import *
from moviepy.editor import VideoClip
from povray_space import SpaceScene, PlanetSystem, Star, Planet
from random import randint


# Camera('location', [100, 50, 100], 'look_at', [0, 0, 0])
scene = SpaceScene(lights=[LightSource([400, 400, 400], 'color', [1, 1, 1])], camera=Camera('location', [500, 500, 500], 'look_at', [0, 0, 0]))
for _ in range(50):
    system = PlanetSystem(circulation_period=randint(100, 500), rotation_center=[randint(10, 200), randint(10, 200), randint(10, 200)],
                          rotation_center_distance=randint(20, 500))
    for i in range(randint(1, 10)):
        planet = Planet(color=[randint(0, 1), randint(0, 1), randint(0, 1)],
                        star_distance=randint(6, 50), planet_system=system, circulation_period=randint(3, 30))
    scene.add_system(system)

scene.show()
