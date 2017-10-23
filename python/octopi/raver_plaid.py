#!/usr/bin/env python

"""A demo client for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

Creates a shifting rainbow plaid pattern by overlaying different sine waves
in the red, green, and blue channels.

To run:
First start the gl simulator using the included "wall" layout

    make
    bin/gl_server layouts/wall.json

Then run this script in another shell to send colors to the simulator

    python_clients/raver_plaid.py

"""

from __future__ import division
import time
import math
import sys
import random
import optparse

try: 
  import json
except ImportError:
  import simplejson as json

import opc
import color_utils


#-------------------------------------------------------------------------------
# handle command line

#client = opc.Client('octo.local:7890')

#if len(sys.argv) == 1:
#    IP_PORT = 'octo.local:7890'
#elif len(sys.argv) == 2 and ':' in sys.argv[1] and not sys.argv[1].startswith('-'):
#    IP_PORT = sys.argv[1]
#else:
#    print('''
#Usage: raver_plaid.py [ip:port]
#
#If not set, ip:port defauls to 127.0.0.1:7890
#''')
#    sys.exit(0)

parser = optparse.OptionParser()
parser.add_option('-l', '--layout', dest='layout', action='store', type='string', help='layout file')
parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890', action='store', type='string', help='ip and port of server')
parser.add_option('-f', '--fps', dest='fps', default=20, action='store', type='int', help='frames per second')

options, args = parser.parse_args()

if not options.layout:
  parser.print_help()
  print
  print 'ERROR: you must specify a goddamn layout file you luddite, using --layout'
  print
  sys.exit(1)

# parse layout file

print
print ' parsing the fucking layout file'
print

coordinates = []
for item in json.load(open(options.layout)):
  if 'point' in item:
    coordinates.append(tuple(item['point']))


#-------------------------------------------------------------------------------
# connect to server

client = opc.Client(options.server)
#client = opc.Client('octo.local:7890')
if client.can_connect():
  print ' connected to %s' % options.server
else:
  print ' NOPE NOPE NOPE: could not connect to %s' % options.server
print


#client = opc.Client(IP_PORT)
#if client.can_connect():
#    print('    connected to %s' % IP_PORT)
#else:
#    # can't connect, but keep running in case the server appears later
#    print('    WARNING: could not connect to %s' % IP_PORT)
#print('')


#-------------------------------------------------------------------------------
# send pixels

print('    sending pixels forever (control-c to exit)...')
print('')

n_pixels = 180  # number of pixels in the included "wall" layout
fps = 60         # frames per second

# how many sine wave cycles are squeezed into our n_pixels
# 24 happens to create nice diagonal stripes on the wall layout
freq_r = 18
freq_g = 18
freq_b = 18

# how many seconds the color sine waves take to shift through a complete cycle
speed_r = 6
speed_g = 6.2
speed_b = 6.4

start_time = time.time()
while True:
    t = (time.time() - start_time) * 3
    pixels = []
    for ii in range(n_pixels):
        pct = (ii / n_pixels)
        # diagonal black stripes
        pct_jittered = (pct * 77) % 33
        blackstripes = color_utils.cos(pct_jittered, offset=t*0.05, period=1, minn=-1.5, maxx=1.5)
        blackstripes_offset = color_utils.cos(t, offset=0.9, period=60, minn=-0.5, maxx=3)
        blackstripes = color_utils.clamp(blackstripes + blackstripes_offset, 0, 1)
        # 3 sine waves for r, g, b which are out of sync with each other
        r = blackstripes * color_utils.remap(math.cos((t/speed_r - pct*freq_r)*math.pi*2), -1, 1, 0, 256)
        g = blackstripes * color_utils.remap(math.cos((t/speed_g - pct*freq_g)*math.pi*2), -1, 1, 0, 256)
        b = blackstripes * color_utils.remap(math.cos((t/speed_b - pct*freq_b)*math.pi*2), -1, 1, 0, 256)
        pixels.append((r, g, b))
    client.put_pixels(pixels, channel=0)
    time.sleep(1 / fps)

