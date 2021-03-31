#!/usr/bin/env python

import logging
import unittest
import redcanary


class Test(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)

        # To hardcode in the info
        # self.client = redcanary.RedCanaryClient('demo', 'xxxxxxxxx')

        # Or use the .env
        self.client = redcanary.RedCanaryClient()

    def test_detections(self):
        print("DETECTIONS")
        for i, detection in enumerate(self.client.detections):
            print(i, detection.headline)

            print('  TIMELINE')
            for entry in detection.timeline:
                print(entry)

            print('  ENDPOINT')
            print('    %s' % detection.endpoint.hostname)
            # force the load of the full object
            print('    %s' % detection.endpoint.operating_system)

            if len(detection.response_plans) > 0:
                print('  RESPONSE PLAN')
                print('    %s' % detection.response_plans[0].state)
                # force the load of the full object
                print('    %s' % detection.response_plans[0].creator)

            if detection.num_indicators > 0:
                print('  INDICATORS')
                i = 0
                for i, indicator in enumerate(detection.indicators):
                    print('    %d %s' % (i, indicator.type))
                self.assertTrue(i == detection.num_indicators - 1)
            print('')

    def test_detections_since(self):
        print("DETECTIONS SINCE")
        second_newest = self.client.detections.next()
        num_since_second_newest = len(self.client.detections(since=second_newest.date))
        self.assertTrue(num_since_second_newest == 1)

        self.assertTrue(len(self.client.detections(since='1970-01-01')) == len(self.client.detections))

    def test_indicators(self):
        print("INDICATORS")
        for i, indicator in enumerate(self.client.indicators):
            print(indicator)
            print(i, indicator.type)
            if len(indicator.detections) > 0:
                # force the load of the full object
                print('  %s' % indicator.detections[0].summary)
                print('')

    def test_limit(self):
        print("LIMIT")
        for type in ['indicators', 'detections', 'endpoints', 'response_plans']:
            collection = getattr(self.client, type)

            print('checking with limit')
            self.assertTrue(len(list(collection(limit=2))) == 2)
            self.assertTrue(len(collection(limit=2)) == 2)

            print('checking with no limit')
            self.assertTrue(len(list(collection(limit=None))) > 2)
            self.assertTrue(len(collection(limit=None)) > 2)

        print('checking normal') # can't be tested above because getattr doesn't get @property
        self.assertTrue(len(list(self.client.indicators)) > 2)
        self.assertTrue(len(self.client.indicators) > 2)

        self.assertTrue(len(list(self.client.detections)) > 2)
        self.assertTrue(len(self.client.detections) > 2)

        self.assertTrue(len(list(self.client.endpoints)) > 2)
        self.assertTrue(len(self.client.endpoints) > 2)

        self.assertTrue(len(list(self.client.response_plans)) > 2)
        self.assertTrue(len(self.client.response_plans) > 2)

    def test_response_plans(self):
        print("RESPONSE_PLANS")
        for i, response_plan in enumerate(self.client.response_plans):
            print("plan %d for detection [%s] on [%s]" % \
                  (i, response_plan.detection.headline, response_plan.endpoint.hostname))

            print('  %s' % response_plan.endpoint.hostname)
            # force the load of the full object
            print('  %s' % response_plan.endpoint.operating_system)

            print('  %s' % response_plan.detection.headline)
            # force the load of the full object
            print('  %s' % response_plan.detection.summary)
            print('')

    def test_endpoints(self):
        print("ENDPOINTS")
        for i, endpoint in enumerate(self.client.endpoints):
            print(i, endpoint.hostname)
            print('  ', endpoint.ip_addresses)
            print('  ', endpoint.sensor)
            print('  ', 'detections (snippets):')
            print('  ', endpoint.detections)
            # force the load of the full object
            if len(endpoint.detections) > 0:
                print('  ', 'first detection - full object:')
                print('  ', endpoint.detections[0].summary)


if __name__ == '__main__':
    unittest.main()
