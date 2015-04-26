import json
import sys
from types import DictType


class Detections(object):
    """Class wrapper for output of Red Canary /detections API route.

    May be used as follows:

    >>> import requests
    >>> from redcanary import detections
    >>> url = 'https://<URL>/openapi/v1/detections.json?auth_token=<API-TOKEN>'
    >>> response = requests.get(url)
    >>> my_detections = detections.Detections(response.content)
    >>> for d in my_detections:
    ...     print d
    """
    def __init__(self, data, as_json=False):
        if as_json == False or type(data) != DictType:
            data = json.loads(data)
        self._detections = data

        self.detection_count = len(self._detections)
        self.position = 0
        
    def __iter__(self):
        return self

    def next(self):
        try:
            ret = Detection(self._detections[self.position]) 
        except IndexError:
            raise StopIteration

        self.position += 1

        return ret


class Detection(object):
    """Class wrapper for a Red Canary detection object returned by the 
    /detections API route.

    May be used as follows:

    >>> my_detection = Detection(json_data)
    >>> print my_detection.date, my_detection.headline
    """
    def __init__(self, data, as_json=False):
        if as_json == False and type(data) != DictType:
            data = json.loads(data)
        self._detection = data

    def __repr__(self):
        return "\n%s %s" % (self.date, self.headline)

    @property
    def id(self):
        id_str = self.headline.split(']')[0]
        return id_str[1:]

    @property
    def date(self):
        return self._detection['date']

    @property
    def dns_hostnames(self):
        return self._detection['host_dns_names']

    @property
    def ip_addresses(self):
        return self._detection['host_ip_addresses']

    @property
    def sensor_group(self):
        ret = None
        try:
            ret = self._detection['host_sensor_groups'][0]
        except IndexError:
            sys.stderr.write("Error: %s missing sensor group")
            ret = None

        return ret

    @property
    def uid(self):
        return self._detection['uid']

    @property
    def headline(self):
        return self._detection['headline']

    @property
    def severity(self):
        return self._detection['severity']

    @property
    def engine_observations(self):
        ret = None
        if len(self._detection['threat_detection_engine_observations']) > 0:
            ret = self._detection['threat_detection_engine_observations']
        
        return ret

    @property
    def details(self):
        return self._detection['details']

    @property
    def root_classification_title(self):
        return self._detection['root_classification_title']
        
    @property
    def subclassification_titles(self):
        ret = None
        if len(self._detection['subclassification_titles']) > 0:
            ret = self._detection['subclassification_titles']
        
        return ret

    @property
    def event_timeline(self):
        return self._detection['event_timeline']

