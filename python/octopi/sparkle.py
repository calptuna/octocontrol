#!/usr/bin/env python

"""A demo client for Open Pixel Control
http://github.com/zestyping/openpixelcontrol

Creates moving blobby colors with sparkles on top.

To run:
First start the gl simulator using, for example, the included "wall" layout

    make
    bin/gl_server layouts/wall.json

Then run this script in another shell to send colors to the simulator

    python_clients/miami.py --layout layouts/wall.json

"""

from __future__ import division
import time
import sys
import optparse
import random
try:
    import json
except ImportError:
    import simplejson as json

import opc 
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

if not options.layout:
    parser.print_help()
    print
    print 'ERROR: you must specify a layout file using --layout'
    print
    sys.exit(1)


#-------------------------------------------------------------------------------
# parse layout file

print
print '    parsing layout file'
print

coordinates = []
for item in json.load(open(options.layout)):
    if 'point' in item:
        coordinates.append(tuple(item['point']))


#-------------------------------------------------------------------------------
# connect to server

#client = opc.Client(options.server)
client = opc.Client('octo.local:7890')
if client.can_connect():
    print '    connected to %s' % options.server
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % options.server
print


#-------------------------------------------------------------------------------
# color function

def pixel_color(t, coord, ii, n_pixels, random_values):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels
    random_values: a list containing a constant random value for each pixel

    Returns an (r, g, b) tuple in the range 0-255

    """
    # make moving stripes for x, y, and z
    x, y, z = coord
#    y += color_utils.cos(x + 0.2*z, offset=0, period=1, minn=0, maxx=0.6)
#    z += color_utils.cos(x, offset=0, period=1, minn=0, maxx=0.3)
#    x += color_utils.cos(y + z, offset=0, period=1.5, minn=0, maxx=0.2)

    # rotate
    x, y, z = y, z, x

#     # shift some of the pixels to a new xyz location
#     if ii % 17 == 0:
#         x += ((ii*123)%5) / n_pixels * 32.12 + 0.1
#         y += ((ii*137)%5) / n_pixels * 22.23 + 0.1
#         z += ((ii*147)%7) / n_pixels * 44.34 + 0.1

    # make x, y, z -> r, g, b sine waves
    r = 0
    g = 0
    b = 0
    #r = color_utils.cos(x, offset=t / 4, period=2.5, minn=0, maxx=1)
    #g = color_utils.cos(y, offset=t / 4, period=2.5, minn=0, maxx=1)
    #b = color_utils.cos(z, offset=t / 4, period=2.5, minn=0, maxx=1)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 1.4)

#    clampdown = (r + g + b)/2
#    clampdown = color_utils.remap(clampdown, 0.4, 0.5, 0, 1)
#    clampdown = color_utils.clamp(clampdown, 0, 1)
#    clampdown *= 0.9
#    r *= clampdown
#    g *= clampdown
#    b *= clampdown

#     # shift the color of a few outliers
#     if random_values[ii] < 0.03:
#         r, g, b = b, g, r

    # black out regions
#    r2 = color_utils.cos(x, offset=t / 10 + 12.345, period=4, minn=0, maxx=1)
#    g2 = color_utils.cos(y, offset=t / 10 + 24.536, period=4, minn=0, maxx=1)
#    b2 = color_utils.cos(z, offset=t / 10 + 34.675, period=4, minn=0, maxx=1)
#    clampdown = (r2 + g2 + b2)/2
#    clampdown = color_utils.remap(clampdown, 0.2, 0.3, 0, 1)
#    clampdown = color_utils.clamp(clampdown, 0, 1)
#    r *= clampdown
#    g *= clampdown
#    b *= clampdown

    # color scheme: fade towards blue-and-orange
#     g = (r+b) / 2
#    g = g * 0.6 + ((r+b) / 2) * 0.4 #warm to cold with holes
#    g = (r+b) / 2 #ice blue -> brief fire
#    r = (g+b) / 2 #toxic green/purple
#    b = ((r+g) / 10) #halloween green blob to fire fire fire
    
    #PURPLE PURPLE PURPLE
#    r = ((g+b) / 2) * 6
#    g = 0
#    b = (r+g) / 2

    #stretched vertical smears
#    v = color_utils.cos(ii / n_pixels, offset=t*0.1, period = 0.07, minn=0, maxx=1) ** 5 * 0.3
#    r += v
#    g += v
#    b += v

#     # stretched vertical smears
#     v = color_utils.cos(ii / n_pixels, offset=t*0.1, period = 0.07, minn=0, maxx=1) ** 5 * 0.3
#     r += v
#     g += v
#     b += v

    # fade behind twinkle
    fade = color_utils.cos(t - ii/n_pixels, offset=0, period=7, minn=0, maxx=1) ** 0.5
    fade = 1 - fade*0.5
    r *= fade
    g *= fade
    b *= fade

    # twinkle occasional LEDs
    twinkle_speed = 0.04
    twinkle_density = 10
    twinkle = (random_values[ii]*7 + time.time()*twinkle_speed) % 1
    twinkle = abs(twinkle*2.2 - 1)
    twinkle = color_utils.remap(twinkle, 0, 1, -1/twinkle_density, 1.1)
    twinkle = color_utils.clamp(twinkle, -0.5, 1.1)
    twinkle **= 12
    twinkle *= color_utils.cos(t - ii/n_pixels, offset=0, period=7, minn=0, maxx=1) ** 0.1
    twinkle = color_utils.clamp(twinkle, -0.1, 1)
    r += twinkle
    g += twinkle
    b += twinkle

    # apply gamma curve
    # only do this on live leds, not in the simulator
    #r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r*256, g*256, b*256)


#-------------------------------------------------------------------------------
# send pixels

print '    sending pixels forever (control-c to exit)...'
print

n_pixels = len(coordinates)
random_values = [random.random() for ii in range(n_pixels)]
start_time = time.time()
while True:
    t = time.time() - start_time
    pixels = [pixel_color(t*0.6, coord, ii, n_pixels, random_values) for ii, coord in enumerate(coordinates)]
    client.put_pixels(pixels, channel=0)
    time.sleep(1 / options.fps)

