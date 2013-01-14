#!/usr/bin/env python2
# Version 0.4
# GIMP plugin to export layers as Sprite for 2D games
#     with their data in json format.
# 0.2: added automatic reverse of image layers
# 0.3: added spacing between frames of the spritesheet
# 0.4: export frames data into a json file

from gimpfu import *
from itertools import product
import json
import os
import logging

gettext.install("gimp20-python", gimp.locale_directory, unicode=True)

def python_sprite_tape_and_json(timg, spacing):
  width = timg.width
  height = timg.height
  jsonfile = os.path.dirname(timg.filename)
  
  alllayers = 0
  for group in timg.layers:
      if isinstance(group, gimp.GroupLayer):
          for layer in group.layers:
              alllayers += 1
              
  spritedata = {"animation": {}}
  
  cnt_hor = 8
  cnt_vert = ((alllayers) / cnt_hor) + 1
  
  newwidth = cnt_hor * width + spacing * (cnt_hor + 1)
  newheight = cnt_vert * height + spacing * (cnt_vert + 1)
  
  timg.resize(newwidth, newheight,0,0)
  x = 0
  y = 0
  state = -1
  
  for group in timg.layers:
      if isinstance(group, gimp.GroupLayer):
          frame = 0
          state += 1
          spritedata["animation"][state] = {}
          for layer in group.layers:
              if isinstance(layer, gimp.Layer):
                  newx = x * width + spacing * (x + 1)
                  newy = y * height + spacing * (y + 1)
                  
                  layer.translate(newx, newy)
                  
                  if x >= cnt_hor:
                      x = 0
                      
                      if y >= cnt_vert:
                          y = 0
                      else:
                          y += 1
                  else:
                      x += 1
                      
                  spritedata["animation"][state][frame] = ((newx, newy),
                                                           (width, height))
                  frame += 1
                  
  pdb.gimp_image_resize_to_layers(timg)
  filename = os.path.join(jsonfile, os.path.splitext(timg.name)[0] + ".json")
  jfile = open(filename, "w")
  data = json.dumps(spritedata, indent=4)
  jfile.write(data)
  jfile.close()
  
register(
  proc_name=("python_fu_sprite_tape_and_json"),
  blurb=("Make the tape of sprites from separate sprites in GroupLayers"),
  help=("Make the tape of sprites from separate sprites in GroupLayers"),
  author=("Shackra Sislock"),
  copyright=("Pheodor Tsapanas a.k.a. FedeX - Shackra Sislock"),
  date=("2013"),
  label=("Sprite tape and json sprite data"),
  imagetypes=("*"),
  params=[
        (PF_IMAGE, "timg", "Image", None),
        (PF_INT, "spacing", "Spacing", 0),
    ],
  results=[],
  function=(python_sprite_tape_json),
  menu=("<Image>/Thomas Aquinas"),
  domain=("gimp20-python", gimp.locale_directory)
  )

main()
