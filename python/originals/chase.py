#!/usr/bin/env python

# Light each LED in sequence, and repeat.

from __future__ import division
import time
import sys 
import optparse
import random
try:
      import json
except ImportError:
      import simplejson as json

import opc, time 
import color_utils

#-------------------------------------------------------------------------------
# command line

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout',
      action='store', type='string',
      help='layout file')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
      action='store', type='string',
      help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=20,
      action='store', type='int',
      help='frames per second')

options, args = parser.parse_args()


# parse layout file
coordinates = []
for item in json.load(open(options.layout)):
  if 'point' in item:
    coordinates.append(tuple(item['point']))


# connect to server
if not options.layout:
      parser.print_help()
      print
      print 'ERROR: you must specify a layout file using --layout'
      print
      sys.exit(1)

numLEDs = 90
client = opc.Client('orbpi.local:7890')
#client = opc.Client(options.server)


# Build chaser(s)
def chaser_thing(t, coord, ii,  n_pixels):

  r = 0
  g = 0
  b = 0

  x, y, z = coord
  spark_ii = (t*9) % n_pixels
  spark_rad = 6
  spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, n_pixels)) / spark_rad)
  spark_val = min(1, spark_val*3)
  r -= spark_val  
  g += spark_val  
  b += spark_val 

  bluerunner_ii = (t*20) % n_pixels
  bluerunner_rad = 3
  bluerunner_val = max(0, (bluerunner_rad - color_utils.mod_dist(ii, bluerunner_ii, n_pixels)) / bluerunner_rad)
  bluerunner_val = min(1, bluerunner_val*3)
  r -= bluerunner_val 
  g -= bluerunner_val
  b += bluerunner_val
  
  redrunner_ii = (t*30) % n_pixels
  redrunner_rad = 3
  redrunner_val = max(0, (redrunner_rad - color_utils.mod_dist(ii, redrunner_ii, n_pixels)) / redrunner_rad)
  redrunner_val = min(1, redrunner_val*3)
  r += redrunner_val 
  g -= redrunner_val
  b -= redrunner_val

  return (r*255, g*255, b*255)


# send pixels
n_pixels = len(coordinates)
start_time = time.time()
while True:
  for i in range(numLEDs):
    t = time.time() - start_time
    pixels = [chaser_thing(t, coord, ii,  n_pixels) for ii, coord in enumerate(coordinates)]

    client.put_pixels(pixels, channel=0)
    #pixels = [ (0,0,0) ] * numLEDs
    #pixels[i] = (20, 120, 255)
    #client.put_pixels(pixels)
    time.sleep(0.03)

