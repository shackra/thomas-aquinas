#!/usr/bin/env python2

from src import scenemanager
from scenes import escena_1
import logging

director = scenemanager.Director()
escena = escena_1.Helloworld(director)
director.changescene(escena)
director.loop()
