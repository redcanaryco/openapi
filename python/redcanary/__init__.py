import os
import sys
import traceback
from restclient import RestClient, Resource

from dotenv import Dotenv


class RedCanaryClient(RestClient):
    def __init__(self, customer_id=None, auth_token=None, **kwargs):
        try:
            # TODO: don't think this is the right location for this file
            # dotenv = Dotenv(os.path.join(os.environ['CWD'], '.env'))
            dotenv = Dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))
            os.environ.update(dotenv)
        except:
            sys.stderr.write('Skipping load of .env...\n')
            sys.stderr.write(traceback.format_exc())

        if not customer_id:
            customer_id = os.environ['RED_CANARY_CUSTOMER_ID']

        if not auth_token:
            auth_token = os.environ['RED_CANARY_AUTH_TOKEN']

        request_options = dict(params={'auth_token': auth_token})
        request_options.update(kwargs.pop('request_options', None) or {})

        RestClient.__init__(self, 'https://%s.my.redcanary.co/openapi/v2' % customer_id,
                            request_options=request_options, **kwargs)

    @property
    def detections(self):
        return Detection(self).all()

    @property
    def endpoints(self):
        return Endpoint(self).all()

    @property
    def indicators(self):
        return Indicator(self).all()

    @property
    def response_plans(self):
        return ResponsePlan(self).all()


class Detection(Resource):
    @property
    def endpoint(self):
        return self.has_one(Endpoint, 'endpoint')

    @property
    def num_indicators(self):
        return self._data['indicators']['count']

    @property
    def indicators(self):
        return Detection(self.client, collection_url=self._data['indicators']['url']).all()

    @property
    def response_plans(self):
        return self.has_many(ResponsePlan, 'response_plans')

    @property
    def timeline(self):
        return self.has_many(DetectionTimelineEntry, 'event_timeline')


class Endpoint(Resource):
    @property
    def detections(self):
        return self.has_many(Detection, 'detections')


class Indicator(Resource):
    @property
    def detections(self):
        return self.has_many(Detection, 'detections')


class ResponsePlan(Resource):
    def __init__(self, client):
        # example of a custom url path (response_plans instead of responseplans)
        Resource.__init__(self, client, resource_path='response_plans')

    @property
    def endpoint(self):
        return self.has_one(Endpoint, 'endpoint')

    @property
    def detection(self):
        return self.has_one(Detection, 'detection')


class DetectionTimelineEntry(Resource):
    @property
    def is_ioc(self):
        return self._data.get('is_ioc', False)

    @property
    def protocol_name(self):
        n = self._data.get('protocol', None)
        if n == '6':
            return 'TCP'
        elif n == '17':
            return 'UDP'

    @property
    def path(self):
        if self.type in ['Process', 'FileModification', 'RegistryModification']:
            return self._data['path']

    def __repr__(self):
        ret = u"\nTimestamp\t%s\n" % self.timestamp

        ret += "Type\t\t"
        if self.is_ioc:
            ret += "IOC "

        ret += "%s" % self.type

        if self.type == 'RegistryModification':
            ret += "\n" # no special type modifier
            ret += "Path\t\t%s" % self.path

        elif self.type == 'FileModification':
            ret += " (%s)\n" % self.modification
            ret += "Path\t\t%s\n" % self.path
            ret += "MD5\t\t%s" % self.md5

        elif self.type == 'Process':
            ret += "\n" # no special type modifier
            ret += "Path\t\t%s\n" % self.path
            ret += "MD5\t\t%s" % self.md5

        elif self.type == 'NetworkConnection':
            ret += " (%s)\n" % self.direction
            ret += "Domain\t\t%s\n" % self.domain
            ret += "IP\t\t%s\n" % self.ip
            ret += "Port\t\t%s\n" % self.port
            ret += "Protocol\t%s" % self.protocol_name

        return ret.encode('UTF-8')
