__author__ = 'Matt Barr'

import spotipy, pprint, sys

spotify = spotipy.Spotify()

name = 'tower of power'

results = spotify.search(q='artist:' + name, type='artist')
items = results['artists']['items']
print len(items)
if len(items) > 0:
    for i in range(len(items)):

        if items[i]['name'] == name:
            print items[i]['name']
            artist = items[i]
    print artist['name'], artist['images'][0]['url'], artist['uri']

