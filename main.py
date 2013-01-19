#!/usr/bin/env python2

from src import scenemanager
from scenes import escena_2
import logging

director = scenemanager.Director()
escena = escena_2.Maitest(director)
director.changescene(escena)
director.loop()
