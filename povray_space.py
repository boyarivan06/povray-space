from vapory import Sphere, Cylinder
from vapory import Texture, Pigment
from vapory import Scene, Camera, LightSource
from moviepy.editor import VideoClip
from math import sin, cos, pi, sqrt
from datetime import datetime
import pyray
from raylib import colors
from planet_system import PlanetSystem
from space_objects import Planet, Star


class SpaceScene:
    def __init__(self, camera=None, systems=None, lights=None):
        if systems is None:
            systems = []
        if camera is None:
            camera = Camera('location', [100, 50, 100], 'look_at', [0, 0, 0])  # 50, 25, 50
        self.camera = camera
        if lights is None and camera is not None:
            lights = [LightSource([100, 50, 100], 'color', [1, 1, 1])]
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
            self.make_png(datetime.now().timestamp(), width, height)
            bcg = pyray.load_image('space.png')
            bcg_texture = pyray.load_texture_from_image(bcg)
            pyray.unload_image(bcg)
            pyray.begin_drawing()
            pyray.clear_background(colors.BLACK)
            pyray.draw_texture(bcg_texture, 0, 0, colors.WHITE)
            pyray.end_drawing()
        pyray.close_window()
