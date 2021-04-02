import logging
import os

from .rest import RestClient

class Detections(RestClient):
    """
    Class for querying Red Canary's Detections APIs
    """

    def __init__(self, customer_id: str = None, auth_token: str = None):
        """
        Parameters
        --------
        customer_id : str
            portal identifier for customer
            if not provided uses env variable RED_CANARY_CUSTOMER_ID
        auth_token : str 
            Red Canary API authorization token
            if not provided uses env variable RED_CANARY_AUTH_TOKEN
        """

        if not customer_id:
            self._customer_id = os.environ['RED_CANARY_CUSTOMER_ID']

        if not auth_token:
            auth_token = os.environ['RED_CANARY_AUTH_TOKEN']


        RestClient.__init__(self, self._customer_id, auth_token)

    @property
    def portal_id(self) -> str:
        return self._customer_id
    
    def all(self, per_page: int = None, since: str = None) -> list:
        """
        Parameters
        --------
        per_page : int
            Number of detections to return per page
            default: 50
        since : str
             Time that limits which detections are returned.
             example: 2018-07-12T12:15:20Z
        """
        return [Detection(i) for i in self._get_all('detections', locals())]
    
class Detection(object):
    """
    Object class for a red canary detection
    """

    def __init__(self, detection: dict):
        """
        Parameters
        --------
        data item : json
        """
        self._detection = detection
    
    @property
    def id(self) -> int:
        """Unique identifier of the detection"""
        return self._detection.get('id')
    
    @property
    def headline(self) -> str:
        """Headline of the detection, including ID and classification"""
        return self._detection.get('attributes').get('headline')

    @property
    def confirmed_at(self) -> str:
        """The date the detection was confirmed"""
        return self._detection.get('attributes').get('confirmed_at')

    @property
    def summary(self) -> str:
        """A summary of information about the detection. May be marked up using Markdown."""
        return self._detection.get('attributes').get('summary')

    @property
    def severity(self) -> str:
        """The severity of the detection as selected by the confirming analyst"""
        return self._detection.get('attributes').get('severity')

    @property
    def last_activity_seen_at(self) -> str:
        """The last time this detection was seen on your system"""
        return self._detection.get('attributes').get('last_activity_seen_at')

    @property
    def classification(self) -> dict:
        """The classification of this detection"""
        return self._detection.get('attributes').get('classification')

    @property
    def time_of_occurrence(self) -> str:
        """The time the detection was confirmed as a threat by Red Canary"""
        return self._detection.get('attributes').get('time_of_occurance')
    
    @property
    def last_acknowledged_at(self) -> str:
        """The time the detection was acknowledged"""
        return self._detection.get('attributes').get('last_acknowledged_at')
    
    @property
    def last_acknowledged_by(self) -> str:
        """The user who acknowledged the detection"""
        return self._detection.get('attributes').get('last_acknowledged_by')

    @property
    def last_remediated_status(self) -> dict:
        """Reason, state, user, and time associated with the remediatied detection"""
        return self._detection.get('attributes').get('last_remediated_status')
    
    @property
    def hostname(self) -> str:
        """The hostname of the endpoint where this detection occurred"""
        return self._detection.get('attributes').get('hostname')

    @property
    def username(self) -> str:
        """The username of the endpoint where this detection occurred"""
        return self._detection.get('attributes').get('username')
    
    @property
    def relationships(self) -> dict:
        """Resources related to this object"""
        return self._detection.get('attributes').get('relationships')