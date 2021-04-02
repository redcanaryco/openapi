import json
import logging
import unittest
import redcanary


class TestDetection(unittest.TestCase):

    def setUp(self):
        with open('test/data/detection.json', 'r') as infile:
            self.detection = json.loads(infile.read())

    def test_object_parsing(self):
        detect_obj = redcanary.Detection(self.detection)

        for key, value in detect_obj.__dict__.get('_detection').items():
            self.assertIsNotNone(value, f"Failed to properly parse {key}")
 

class TestDemoDetections(unittest.TestCase):
    
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        
        self.client = redcanary.Detections()

        if not self.client.portal_id == 'demo':
            self.skipTest("Requires access to RC's demo environemnt")



    def test_all_dections(self):
        self.all_detections = self.client.all()
        self.assertEqual(len(self.all_detections), 243, 
            f"Failed to find expected number of detections, expected 243")

    def test_since_param(self):
        self.assertEqual(len(self.client.all(since="2019-01-01T00:00:00Z")), 25,
            "Since parameter didn't generate the correct number of detections")
    
    def test_live_detection_parsing(self):
        detect_obj = self.client.all(since="2020-01-01T00:00:00Z")[0]
        for key, value in detect_obj.__dict__.get('_detection').items():
            self.assertIsNotNone(value, f"Failed to properly parse {key}")

if __name__ == '__main__':
    unittest.main()