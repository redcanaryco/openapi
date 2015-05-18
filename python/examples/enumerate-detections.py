#!/usr/bin/env python

#import datetime

import redcanary


if __name__ == '__main__':

#    now = datetime.datetime.now()
#    timedelta = datetime.timedelta(days=-7)

    rc = redcanary.RedCanaryClient()

    for detection in rc.detections:
        print detection.headline
        print '\tDate: %s' % detection.date
        print '\tSeverity: %s' % detection.severity
        print '\tHostname: %s' % detection.endpoint.hostname
        print '\tUsername: %s' % detection.user['name']
        
