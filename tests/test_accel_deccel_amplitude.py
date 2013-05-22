# coding: utf-8
from pyglet import gl
import pyglet
from summa.director import director
from summa.actions import grid3d_actions, basegrid_actions
from summa.layer import Layer
import os

import customstuff

pyglet.resource.path.append(
    os.path.join(os.path.dirname(os.path.realpath(__file__))))
pyglet.resource.reindex()

testinfo = "s, t 3.0, s, t 5.0, s, t 10.0, s, q"
tags = "grid_actions, AccelDeccelAmplitude, Waves3D"

class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()
        self.img = pyglet.resource.image('background_image.png')

    def draw( self ):
        gl.glColor4ub(255, 255, 255, 255)
        gl.glPushMatrix()
        self.transform()
        self.img.blit(0,0)
        gl.glPopMatrix()

def test_accel_deccel_amplitude():
    director.init( resizable=True )
    main_scene = customstuff.TimedScene()
    main_scene.add( BackgroundLayer(), z=0 )

    # In real code after a sequence of grid actions the StopGrid() action
    # should be called. Omited here to stay in the last grid action render
    action1 = grid3d_actions.Waves3D(waves=16, amplitude=80,
                                     grid=(16,16), duration=10)
    action2 = basegrid_actions.AccelDeccelAmplitude(action1, rate=4.0)

    main_scene.do(action2)
    director.run (main_scene)
