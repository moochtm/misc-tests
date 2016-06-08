__author__ = 'Matt Barr'

import soco

sonos = list(soco.discover())[0]

q = sonos.get_queue()

print q[0].item_id