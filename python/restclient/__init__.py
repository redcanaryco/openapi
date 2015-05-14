import logging
import requests


class RestClient(object):
    """
    A client for connecting to a REST API
    """

    def __init__(self, base_url, request_options=None):
        """
        Creates a new client.
        base_url: the base url of the server
        request_options: options that should be passed to requests.* calls (ssl_verify, params, etc.)
        """
        self._base_url = base_url
        self._request_options = request_options

    @property
    def base_url(self):
        return self._base_url

    @property
    def request_options(self):
        return self._request_options


class Resource(object):
    """
    A resource that can be retrieved through the API. Should be subclassed:

        class Animal(Resource):
            pass

    Then you can get all the animals:

        Animal(client).all()

    Or just one by ID:

        Animal(client).find(7)

    """
    client = None
    resource_path = None

    def __init__(self, client, resource_path=None, collection_url=None):
        """
        Creates a way to get the Resource via all() and find()
        """
        # print "New %s, client: %s, data: %s" % (self.__class__.__name__, client, data)
        Resource.client = client
        Resource.resource_path = resource_path or (self.__class__.__name__.lower() + 's')
        Resource.collection_url = collection_url or ("%s/%s" % (Resource.client.base_url, Resource.resource_path))

    @classmethod
    def all(cls):
        """
        Returns an iterator for iterating through the collection of resources
        """
        # TODO: 1) paginate and 2) since
        return list([cls._build(data, is_snippet=False) for data in cls._request(cls.collection_url)])

    @classmethod
    def find(cls, id):
        """
        Finds a resource by ID
        """
        return cls._build(cls._request("%s/%d" % (cls.collection_url, id)), is_snippet=False)

    @classmethod
    def _build(cls, data, is_snippet):
        """
        Builds an object from the JSON data received from the API
        """
        object = cls(cls.client)
        object._load_from_data(data, is_snippet)
        return object

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        elif self._is_snippet:
            # we are only a snippet, so we need to get the full object info
            self._load_from_data(self._request(self.url), is_snippet=False)
            # and then get the attribute again
            return self.__getattr__(name)
        else:
            raise AttributeError("No such attribute: " + name)

    def _load_from_data(self, data, is_snippet=False):
        self.__setattr__('_data', data)
        self.__setattr__('_is_snippet', is_snippet)

    def _has_many_snippets(self, klass, field_name):
        return list([klass._build(snippet, is_snippet=True) for snippet in self._data[field_name]])

    def _has_one_snippet(self, klass, field_name):
        return klass._build(self._data[field_name], is_snippet=True)

    def __repr__(self):
        return object.__repr__(self) + ":" + self._data.__repr__()

    @classmethod
    def _request(cls, url):
        logging.debug("GET [%s]" % url)
        response = requests.get(url, **cls.client._request_options)
        logging.debug(response.url)
        response.raise_for_status()
        return response.json()
