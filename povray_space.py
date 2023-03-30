from vapory import Sphere, Cylinder
from vapory import Texture, Pigment
from vapory import Scene, Camera, LightSource
from moviepy.editor import VideoClip
from math import sin, cos, pi, sqrt
from datetime import datetime
import pyray
from raylib import colors


class Planet:
    def __init__(self, radius=2, star_distance=6, color=None, planet_system=None, circulation_period=10):

        if planet_system is None:
            self.system_center = [0, 0, 0]
        else:
            planet_system.add_planet(self)
            self.system_center = planet_system.center

        if color is None:
            self.texture = Texture(Pigment('color', [1, 1, 1]))
        else:
            self.texture = Texture(Pigment('color', color))
        self.radius = radius
        self.star_distance = star_distance
        self.circulation_period = circulation_period

    def assemble(self, time):
        angle = pi * time / self.circulation_period
        return Sphere([self.system_center[0] + sin(angle) * self.star_distance, self.system_center[1],
                       self.system_center[2] + cos(angle) * self.star_distance], self.radius, self.texture)


class Star:
    def __init__(self, radius=3, color=None, planet_system=None):
        if planet_system is None:
            self.system_center = [0, 0, 0]
        else:
            self.system_center = planet_system.center
        if color is None:
            self.texture = Texture(Pigment('color', [1, 1, 1, .8]))
        else:
            self.texture = Texture(Pigment('color', color))
        self.radius = radius

    def assemble(self):
        return Sphere(self.system_center, self.radius, self.texture)


class PlanetSystem:
    def __init__(self, rotation_center=None, rotation_center_distance=0,
                 star=None, planets=None, circulation_period=100, angle=0):
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
        if planets is None:
            planets = []
        else:
            for n, planet in enumerate(planets):
                planets[n].system_center = self.center
        self.planets = planets

    def assemble(self, time):
        angle = pi * time / self.circulation_period
        self.center = [self.rotation_center[0] + sin(angle) * self.rotation_center_distance, self.rotation_center[1],
                       self.rotation_center[2] + cos(angle) * self.rotation_center_distance]
        result = [self.star.assemble(), LightSource(self.center, 'color', [1, 1, 1])] + \
                 [planet.assemble(time) for planet in self.planets]
        return result

    def add_planet(self, planet):
        self.planets.append(planet)
        planet.system_center = self.center


class SpaceScene:
    def __init__(self, camera=None, systems=None, lights=None):
        if systems is None:
            systems = []
        if camera is None:
            camera = Camera('location', [50, 25, 50], 'look_at', [0, 0, 0])
        self.camera = camera
        if lights is None:
            lights = []  # [LightSource([20, 20, 20], 'color', [1, 1, 1])]
        self.systems = systems
        self.lights = lights

    def add_system(self, system):
        self.systems.append(system)

    def assemble(self, time):
        objects = []
        for system in self.systems:
            objects += system.assemble(time)
        # print('objects:', *objects)
        return Scene(self.camera, objects+self.lights)

    def make_frame(self, time, width=500, height=500):
        scene = self.assemble(time)
        return scene.render(width=width, height=height, antialiasing=0.001)

    def make_gif(self, duration=10, filename=None, fps=20):
        if filename is None:
            filename = f'space{datetime.now()}.gif'
        else:
            filename = filename.split('.')[0] + '.gif'
        VideoClip(self.make_frame, duration=duration).write_gif(filename, fps)

    def make_png(self, time, width=500, height=500):
        scene = self.assemble(time)
        scene.render(outfile='space.png', width=width, height=height)

    def show(self, width=500, height=500):
        pyray.init_window(width, height, 'space')
        while not pyray.window_should_close():
            self.make_png(datetime.now().timestamp())
            bcg = pyray.load_image('space.png')
            bcg_texture = pyray.load_texture_from_image(bcg)
            pyray.unload_image(bcg)
            pyray.begin_drawing()
            pyray.clear_background(colors.BLACK)
            pyray.draw_texture(bcg_texture, 0, 0, colors.WHITE)
            pyray.end_drawing()
        pyray.close_window()
