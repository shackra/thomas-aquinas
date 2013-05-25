# coding: utf-8

testinfo = "s, q"
tags = "transform_anchor, scale, zoom"

from summa.director import director
from summa.sprite import Sprite
from summa.layer import ColorLayer

from customstuff import TimedScene

def test_anchors():
    director.init( resizable=True )
    main_scene = TimedScene()

    white = ColorLayer(255,255,255,255)
    red = ColorLayer(255,0,0,255)
    blue = ColorLayer(0,0,255,255)
    green = ColorLayer(0,255,0,255)

    x, y = director.get_window_size()

    red.scale = 0.75
    blue.scale = 0.5
    blue.transform_anchor = 0, 0
    green.scale = 0.25
    green.transform_anchor = x,y

    red.add( Sprite( 'grossini.png', (0, y/2) ), z=1 )
    blue.add( Sprite( 'grossini.png', (0, y/2) ), z=1 )
    green.add( Sprite( 'grossini.png', (0, y/2) ), z=1 )
    red.add( Sprite( 'grossini.png', (x, y/2) ), z=1 )
    blue.add( Sprite( 'grossini.png', (x, y/2) ), z=1 )
    green.add( Sprite( 'grossini.png', (x, y/2) ), z=1 )

    main_scene.add( white, z=0 )
    main_scene.add( red, z=1 )
    main_scene.add( blue, z=2 )
    main_scene.add( green, z=3 )

    director.run (main_scene)
