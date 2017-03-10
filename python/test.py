#!/usr/bin/python3

import tevreden
import pprint

t = tevreden.APIClient( platform = 'onderzoek', api_key = 'YZdkefMmJl4MhSpwcmFS5gzxpJ0ppK08', domain = 'api.lennart.dev.tevreden.nl', ssl_insecure = True )

platforms = t.get_platforms()
for platform in platforms:
    print(platform['name'])
    
stats = t.call( path = '/statistics' )
pprint.pprint(stats)

locations = t.get_locations({'q': 'excellence'})
pprint.pprint(locations);

location = t.get_location( 'TeVrEdN2016' )
pprint.pprint(location);

location = t.get_location( 'BESTAATNIET' )
pprint.pprint(location);
