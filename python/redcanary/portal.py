import requests

from redcanary.detections import Detections, Detection
from redcanary.timeline import Timeline, TimelineEntry

EPOCH = '1970-01-01T00:00:00-00'

DOMAIN='my.redcanary.co'
BASE_URI='openapi/v2'   

class Portal:
    def __init__(self, rc_customer_id, rc_api_key):
        self.rc_customer_id = rc_customer_id
        self.rc_api_key = rc_api_key
        
        self.domain = DOMAIN
        self.base_uri = BASE_URI

        self.since = EPOCH

    @property
    def base_url(self):
        url = 'https://%s.%s/%s/' % (self.rc_customer_id,
                                     self.domain,
                                     self.base_uri)
        return url
    
    def get_detections(self):
        url = '%s/detections.json?auth_token=%s&since=%s' % (self.base_url, 
                                                             self.rc_api_key,
                                                             self.since)
        response = requests.get(url)
        return Detections(response.content)
        
