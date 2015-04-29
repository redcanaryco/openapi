#!/usr/bin/env python

import os
import sys

try:
    import requests
except:
    print "'pip install requests' to proceed . . ."
    sys.exit(1)

try:
    import dotenv
    dotenv.read_dotenv()
except:
    sys.stderr.write("'pip install django-dotenv' to use .env file\n")

from redcanary.detections import Detections, Detection
from redcanary.timeline import Timeline, TimelineEntry


ENV_ERROR = """\nRC_CUSTOMER_ID and/or RC_API_KEY environment variables not found.

These environment variables may be set manually, or you can opt to use something
like dotenv ('pip install django-dotenv'), which allows them to be stored in a 
file."""


if __name__ == '__main__':

    try:
        rc_customer_id = os.environ.get("RC_CUSTOMER_ID")
        rc_api_key = os.environ.get("RC_API_KEY")
    except:
        sys.stderr.write(ENV_ERROR)
        sys.exit(1)

    url = 'https://%s.my.redcanary.co/openapi/v2/detections.json?auth_token=%s' \
        % (rc_customer_id, rc_api_key)

    response = requests.get(url)
    detections = Detections(response.content)

    for detection in detections:
        print '---------------------------------------------------------------'
        print detection.headline
        print '---------------------------------------------------------------'
        for event in detection.event_timeline:
            print event
        print ''
        
