#!/usr/bin/env python

import sys

try:
    import requests
except:
    print "'pip install requests' to proceed . . ."
    sys.exit(1)

from redcanary.detections import Detections, Detection
from redcanary.timeline import Timeline, TimelineEntry

### CHANGE ME ###
CUSTOMER_ID = ''
API_KEY = ''

if __name__ == '__main__':

    if len(API_KEY) == 0 or len(CUSTOMER_ID) == 0:
        print "Please check customer ID and API key variables!"
        sys.exit(1)

    url = 'https://%s.my.redcanary.co/openapi/v1/detections.json?auth_token=%s' \
        % (CUSTOMER_ID, API_KEY)

    response = requests.get(url)
    detections = Detections(response.content)

    for detection in detections:
        print '---------------------------------------------------------------'
        print detection.headline
        print '---------------------------------------------------------------'
        timeline = Timeline(detection.event_timeline)
        for event in timeline:
            print event
        print ''
        
