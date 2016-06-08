__author__ = 'Matt Barr'

import soco
from pprint import pprint
import json

from soco.plugins.spotify import Spotify, SpotifyTrack

def json_pprint(thing):
    print(json.dumps(thing, indent = 4))

from soco.music_services import MusicService

zone_list = list(soco.discover())
sonos = zone_list[0]

print(MusicService.get_subscribed_services_names())

spotify = MusicService('Spotify')

print(spotify.available_search_categories)

search_term = 'Corinne Bailey Rae'
result = spotify.search(category='artists', term=search_term)
print result
for search_result in result['mediaCollection']:
    if search_result['title'] == search_term:
        print search_result
        json_pprint(spotify.get_metadata(search_result['id']))
        b_resultlist = spotify.get_metadata(search_result['id'])
        for b_result in b_resultlist['mediaCollection']:
            if b_result['title'] == 'Top Tracks':
                #json_pprint(spotify.get_metadata(b_result['id']))
                c_resultlist = spotify.get_metadata(b_result['id'])
    #print result['mediaCollection']#[search_result]

#sonos.add_uri_to_queue(c_resultlist['mediaMetadata'][0]['id'])
st = SpotifyTrack(c_resultlist['mediaMetadata'][0]['id'])
print(st.didl_metadata)
#spotify_plugin = Spotify(soco)
#spotify_plugin.add_track_to_queue(st)
