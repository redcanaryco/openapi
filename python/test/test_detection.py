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

        for name in [n for n in dir(detect_obj) if not n.startswith('_')]:
            self.assertIsNotNone(detect_obj.__getattribute__(name), f"Failed to properly parse {name}")

class TestDetector(unittest.TestCase):

    def setUp(self):
        with open('test/data/detector.json', 'r') as infile:
            self.detector = json.loads(infile.read())

    def test_object_parsing(self):
        detector_obj = redcanary.Detector(self.detector)

        for name in [n for n in dir(detector_obj) if not n.startswith('_')]:
            self.assertIsNotNone(detector_obj.__getattribute__(name), f"Failed to properly parse {name}")

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
        for name in [n for n in dir(detect_obj) if not n.startswith('_')]:
            self.assertIsNotNone(detect_obj.__getattribute__(name), f"Failed to properly parse {name}")


if __name__ == '__main__':
    unittest.main()