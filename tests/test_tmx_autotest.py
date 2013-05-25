# coding: utf-8

testinfo = "s, t 1.1, s, t 2.1, s, t 3.1, s, t 4.1, s, t 5.1, s, t 6.1, s, q"
tags = "scrolling, ScrollingManager, TMX"

import pyglet
pyglet.resource.path.append(pyglet.resource.get_script_home())
pyglet.resource.reindex()

from summa import tiles, layer
from summa.actions import CallFunc, ScaleTo, Delay
from summa.director import director

from customstuff import TimedScene

class TestScene(TimedScene):
    def __init__(self):
        super(TestScene, self).__init__()
        scroller = layer.ScrollingManager()
        scrollable = tiles.load('road-map.tmx')['map0']
        scroller.add(scrollable)
        self.add(scroller)
        template_action = ( CallFunc(scroller.set_focus, 0, 0) + Delay(1) +
                            CallFunc(scroller.set_focus, 768, 0) + Delay(1) +
                            CallFunc(scroller.set_focus, 768, 768) +Delay(1) +
                            CallFunc(scroller.set_focus, 1500, 768) +Delay(1) +
                            ScaleTo(0.75, 1) + Delay(1) +
                            CallFunc(scrollable.set_debug, True) + Delay(1) +
                            CallFunc(director.window.set_size, 800, 600)
        )
        scroller.do(template_action)

def test_tmx():
    director.init(width=600, height=300, do_not_scale=True, resizable=True)
    main_scene = TestScene()
    director.run(main_scene)
