#!/usr/bin/env python

import redcanary


if __name__ == '__main__':

    rc = redcanary.RedCanaryClient()

    for endpoint in rc.endpoints:
        print(endpoint.hostname)

        # Iterate over all items in the endpoint data repository.
        for k,v in endpoint.data.iteritems():

            # Print sensor-specific data.
            if k == 'sensor':
                print('\tSensor data:')
                for sk,sv in v.iteritems():
                    print('\t\t%s: %s' % (sk, sv))

            # Print detection headlines associated with this endpoint.
            elif k == 'detections' and len(endpoint.detections) > 0:
                print('\tDetections:')
                for detection in endpoint.detections:
                    print('\t\t%s' % detection.headline)

            # Print everything else.
            else:
                print('\t%s: %s' % (k, v))


        
