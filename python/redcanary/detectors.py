class Detector(object):
    """
    Object class for a red canary detector
    """

    def __init__(self, detector: dict):
        """
        Parameters
        --------
        data item : json
        """
        self._detector = detector
        self._attributes = detector.get('attributes')

    @property
    def id(self) -> int:
        """Unique identifier of the detector"""
        return self._detector.get('id')
    
    @property
    def name(self) -> str:
        """Name of the Red Canary detector"""
        return self._attributes.get('name')
    
    @property
    def description(self) -> str:
        """Description of the activity the detector identifies in Markdown format"""
        return self._attributes.get('description')
    
    @property
    def contributing_intelligence(self) -> str:
        """The type of adversary intelligence supporting this detector."""
        return self._attributes.get('contributing_intelligence')

    @property
    def attack_technique_identifiers(self) -> list:
        """The specific ATT&CK Techniques the detector maps to"""
        return self._attributes.get('attack_technique_identifiers', [])

    @property
    def relationships(self) -> dict:
        """Resources related to this object"""
        return self._detector.get('relationships')
