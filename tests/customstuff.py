# coding: utf-8
from summa.director import director
from summa.scene import Scene
import pyglet

class TimedScene(Scene):
    def __init__(self, *children):
        super(TimedScene, self).__init__(*children)
        self._dt = 0
        self._maxtime = 20
        self._next_scene = None
        self._changetype = 0
        self.schedule(self.timeit)

    def changescene(self):
        if self._next_scene is None:
            pyglet.app.exit()

        if self._changetype == 0:
            director.push(self._next_scene)
        elif self._changetype == 1:
            self._next_scene = None
            director.pop()
        elif self._changetype == 2:
            director.replace(self._next_scene)
        elif self._changetype == 3:
            self._next_scene = None
            director.scene.end(True)

    def timeit(self, dt):
        if self._dt >= self._maxtime:
            self._dt = 0
            self.changescene()
        else:
            self._dt += dt

    def setnextscene(self, change, scene):
        self._next_scene = scene
        self._changetype = change

    def setmaxtime(self, maxtime):
        self._maxtime = maxtime
