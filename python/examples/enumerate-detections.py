#!/usr/bin/env python

import redcanary
import logging


if __name__ == '__main__':

    logging.root.setLevel(logging.WARN)

    # Set up an instance of the Red Canary client.
    #
    # If intercepting SSL or dealing with certs that don't validate:
    #   rc = redcanary.RedCanaryClient(request_options={'verify': False})
    #
    # The request_options get passed directly to requests, so other options
    # may be used as needed.
    rc = redcanary.RedCanaryClient()

    # Iterate over detections. 
    #
    # Optionally pass a starting date to limit the number of results:
    #   for detection in rc.detections(since='2015-01-20T00:00:01'):
    # 
    # To output the entire detection as JSON, write detection.as_json to a
    # file or stdout. 
    for detection in rc.detections:
        print(detection.headline)
        print('\tDate: %s' % detection.date)
        print('\tSeverity: %s' % detection.severity)

