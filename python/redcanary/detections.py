import logging
import os
import sys

from .rest import RestClient
from .detectors import Detector

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
        self._customer_id = customer_id
        self._auth_token = auth_token

        if not self._customer_id:
            try:
                self._customer_id = os.environ['RED_CANARY_CUSTOMER_ID']
            except KeyError:
                pass

        if not self._auth_token:
            try:
                self._auth_token = os.environ['RED_CANARY_AUTH_TOKEN']
            except KeyError:
                pass

        if not self._customer_id or not self._auth_token:
            raise ValueError("API token or customer id not provided or found as environment variable")
        
        RestClient.__init__(self, self._customer_id, self._auth_token)


        self._str_remediation_options = [
            "remediated",
            "not_remediated_false_positive",
            "not_remediated_sanctioned_activity",
            "not_remediated_unwarranted"
        ]
        self.REMEDIATED = self._str_remediation_options[0]
        self.FALSE_POSITIVE = self._str_remediation_options[1]
        self.SANCTIONED_ACTIVITY = self._str_remediation_options[2]
        self.UNWANTED = self._str_remediation_options[3]

    @property
    def portal_id(self) -> str:
        return self._customer_id
    
    def all(self, per_page: int = None, since: str = None) -> list:
        """
        Pulls all detections matching the provided parameters

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

    def by_id(self, id: int) -> object:
        """
        Searches for detection by id

        Parameters
        --------
        id : int
            detection id
        """
        return Detection(self._get_by_id('detections', id))

    def detectors(self, detection: object) -> list:
        """
        Pulls detectors associated with a particular detection

        Parameters
        --------
        detection : Detection
            single detection object
        """
        # pull out the full and partial paths to query
        full_url = detection.links.get('detectors').get('href')
        api_path = ('/').join(full_url.split('/')[5:])
        detection.detectors = [Detector(i) for i in self._get_all(api_path)]
        return detection

    def acknowledge(self, id: int) -> object:
        """
        You can mark a detection as acknowledged to inform your team. Returns detection object

        Parameters
        --------
        id : Red Canary detection id 
        """
        str_api_path = f"detections/{id}/mark_acknowledged"
        
        return Detection(self._patch_request(str_api_path))
    
    def update_remediation(self, id: int, state: str, comment: str = ""):
        """
        You can update a detection's remediation state.
        Parameters
        --------
        id : Red Canary detection id 
        state : remediated, not_remediated_false_positive, not_remediated_sanctioned_activity, not_remediated_unwarranted
        comment: (optional) Comment describing the reason why the detection was remediated in this manner
        """
        # Make sure only approved states were provided
        if not state in self._str_remediation_options:
            raise ValueError(f'State {state} not in {self._str_remediation_options}')
        
        str_api_path = f"detections/{id}/update_remediation_state"
        params = dict()
        params.update({
            "remediation_state" : state,
            "comment" : comment
        })
        return Detection(self._patch_request(str_api_path, params=params))


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
        self._attributes = detection.get('attributes')
    
    @property
    def id(self) -> int:
        """Unique identifier of the detection"""
        return self._detection.get('id')
    
    @property
    def headline(self) -> str:
        """Headline of the detection, including ID and classification"""
        return self._attributes.get('headline')

    @property
    def confirmed_at(self) -> str:
        """The date the detection was confirmed"""
        return self._attributes.get('confirmed_at')

    @property
    def summary(self) -> str:
        """A summary of information about the detection. May be marked up using Markdown."""
        return self._attributes.get('summary')

    @property
    def severity(self) -> str:
        """The severity of the detection as selected by the confirming analyst"""
        return self._attributes.get('severity')

    @property
    def last_activity_seen_at(self) -> str:
        """The last time this detection was seen on your system"""
        return self._attributes.get('last_activity_seen_at')

    @property
    def classification(self) -> dict:
        """The classification of this detection"""
        return self._attributes.get('classification')

    @property
    def time_of_occurrence(self) -> str:
        """The time the detection was confirmed as a threat by Red Canary"""
        return self._attributes.get('time_of_occurrence')

    @property
    def last_acknowledged_at(self) -> str:
        """The time the detection was acknowledged"""
        return self._attributes.get('last_acknowledged_at')
    
    @property
    def last_acknowledged_by(self) -> str:
        """The user who acknowledged the detection"""
        return self._attributes.get('last_acknowledged_by')

    @property
    def last_remediated_status(self) -> dict:
        """Reason, state, user, and time associated with the remediatied detection"""
        return self._attributes.get('last_remediated_status', dict({"remediation_state": "Not remediated"}))
    
    @property
    def hostname(self) -> str:
        """The hostname of the endpoint where this detection occurred"""
        return self._detection.get('hostname')

    @property
    def username(self) -> str:
        """The username of the endpoint where this detection occurred"""
        return self._detection.get('username')
    
    @property
    def relationships(self) -> dict:
        """Resources related to this object"""
        return self._detection.get('relationships')

    @property
    def links(self) -> dict:
        """Resources associated with this object"""
        return self._detection.get('links')
