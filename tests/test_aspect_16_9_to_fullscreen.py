# coding: utf-8

testinfo = "s, q"
tags = "resize, resizable, aspect ratio, set_caption"

from pyglet import gl
import summa
from summa.director import director

from customstuff import TimedScene

width = 768
height = 480
assert abs(width/float(height)-16/10.0)<0.0001

class ProbeRect(summa.summanode.SummaNode):
    def __init__(self, width, height, color4):
        super(ProbeRect,self).__init__()
        self.color4 = color4
        w2 = int(width/2)
        h2 = int(height/2)
        #self.vertexes = [(-w2,h2,0),(w2,h2,0), (w2,-h2,0),(-w2,-h2,0)]
        self.vertexes = [(0,0,0),(0,height,0), (width,height,0),(width,0,0)]

    def draw(self):
        gl.glPushMatrix()
        self.transform()
        gl.glBegin(gl.GL_QUADS)
        gl.glColor4ub( *self.color4 )
        for v in self.vertexes:
            gl.glVertex3i(*v)

        gl.glEnd()
        gl.glPopMatrix()

class TestLayer(summa.layer.Layer):
    def __init__(self):
        super(TestLayer, self).__init__()
        self.add( ProbeRect(width, height, (0,0,255,255)), z=1)
        border_size = 10
        inner = ProbeRect(width-2*border_size, height-2*border_size,
                          (255,0,0,255))
        inner.position = (border_size, border_size)
        self.add(inner, z=2 )
        outer = ProbeRect(width+2*border_size, height+2*border_size,
                          (255,255,0,255))
        outer.position = (-border_size, -border_size)
        self.add(outer, z=0 )

description = """
Starts a 16/10 aspect ratio window.
CTRL-F toggles fullscreen

The scene draw three boxes, centered at the window center.
  blue box: the exact same size as the window
  yellow box: a little bigger than blue box
  red box: a little smaller than blue box
Draw order is yellow, blue, red
You must see no yellow, and a red rectangle with equal sized blue borders
"""

def test_aspect_16_9_to_fullscreen():
    print description
    director.init( width=width, height=height, resizable=False )
    director.window.set_caption('aspect ratio and fullscreen'
                                ' - see console for usage')
    scene = TimedScene()
    scene.add(TestLayer())
    director.run( scene )
