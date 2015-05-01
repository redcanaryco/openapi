#!/usr/bin/env python

import datetime
import os
import sys

try:
    import dotenv
    dotenv.read_dotenv()
except:
    sys.stderr.write("'pip install django-dotenv' to use .env file\n")

from redcanary.detections import Detections, Detection
from redcanary.portal import Portal
from redcanary.timeline import Timeline, TimelineEntry


ENV_ERROR = "\nRC_CUSTOMER_ID and/or RC_API_KEY environment variables not found."


if __name__ == '__main__':

    try:
        rc_customer_id = os.environ.get("RC_CUSTOMER_ID")
        rc_api_key = os.environ.get("RC_API_KEY")
    except:
        sys.stderr.write(ENV_ERROR)
        sys.exit(1)

    now = datetime.datetime.now()
    timedelta = datetime.timedelta(days=-7)

    p = Portal(rc_customer_id, rc_api_key)
    p.since = now + timedelta
    detections = p.detections()

    for detection in detections:
        print '---------------------------------------------------------------'
        print detection.headline
        print '---------------------------------------------------------------'
        for event in detection.event_timeline:
            print event
        print ''
        
