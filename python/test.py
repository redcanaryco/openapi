#!/usr/bin/env python

import unittest
import redcanary


class Test(unittest.TestCase):
    def setUp(self):
        #logging.basicConfig(level=logging.DEBUG)

        # To hardcode in the info
        # self.client = redcanary.RedCanaryClient('demo', 'xxxxxxxxx')

        # Or use the .env
        self.client = redcanary.RedCanaryClient()

    def test_detections(self):
        print "DETECTIONS"
        for detection in self.client.detections:
            print detection.headline

            print '  TIMELINE'
            for entry in detection.timeline:
                print entry

            print '  ENDPOINT'
            print '    %s' % detection.endpoint.hostname
            # force the load of the full object
            print '    %s' % detection.endpoint.operating_system

            if len(detection.response_plans) > 0:
                print '  RESPONSE PLAN'
                print '    %s' % detection.response_plans[0].state
                # force the load of the full object
                print '    %s' % detection.response_plans[0].creator

            if detection.num_indicators > 0:
                print '  INDICATORS'
                for indicator in detection.indicators:
                    print '    %s' % indicator.type
            print ''

    def test_indicators(self):
        print "INDICATORS"
        for indicator in self.client.indicators:
            print indicator.type
            # force the load of the full object
            if len(indicator.detections) > 0:
                print '  %s' % indicator.detections[0].summary
                print ''

    def test_response_plans(self):
        print "RESPONSE_PLANS"
        for response_plan in self.client.response_plans:
            print "plan for detection [%s] on [%s]" % \
                  (response_plan.detection.headline, response_plan.endpoint.hostname)

            print '  %s' % response_plan.endpoint.hostname
            # force the load of the full object
            print '  %s' % response_plan.endpoint.operating_system

            print '  %s' % response_plan.detection.headline
            # force the load of the full object
            print '  %s' % response_plan.detection.summary
            print ''

    def test_endpoints(self):
        print "ENDPOINTS"
        for endpoint in self.client.endpoints:
            print endpoint.hostname
            print '  ', endpoint.ip_addresses
            print '  ', endpoint.sensor
            print '  ', 'detections (snippets):'
            print '  ', endpoint.detections
            # force the load of the full object
            if len(endpoint.detections) > 0:
                print '  ', 'first detection - full object:'
                print '  ', endpoint.detections[0].summary
            print
            #
            #         # code.interact(local=locals())
    

if __name__ == '__main__':
    unittest.main()
