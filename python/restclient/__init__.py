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
        return PaginatedCollection(cls)

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
        # snippets are not paginated
        return list([klass._build(snippet, is_snippet=True) for snippet in self._data[field_name]])

    def _has_one_snippet(self, klass, field_name):
        return klass._build(self._data[field_name], is_snippet=True)

    def __repr__(self):
        return object.__repr__(self) + ":" + self._data.__repr__()

    @classmethod
    def _request(cls, url, query_params=None):
        logging.debug("GET [%s]" % url)

        request_options = cls.client._request_options.copy()
        if query_params:
            request_options['params'].update(query_params)

        response = requests.get(url, **request_options)
        logging.debug(response.url)
        response.raise_for_status()
        return response.json()

    @classmethod
    def _request_paginated(cls, url, query_params=None, page=0, header_total_items_key='total'):
        logging.debug("GET PAGE %d [%s]" % (page, url))

        request_options = cls.client._request_options.copy()
        if query_params:
            request_options['params'].update(query_params)
        request_options['params']['page'] = page

        response = requests.get(url, **request_options)
        logging.debug(response.url)
        return response.json(), int(response.headers[header_total_items_key]), response.links


class PaginatedCollection(object):
    def __init__(self, resource):
        self.resource = resource

        self.current_page_num = None
        self.current_page_size = None
        self.current_page_raw_items = None
        self.current_page_position = None
        self.overall_position = 0
        self._size = None

        # params set through __call__
        self.limit = None
        self.query_params = {}

    def __call__(self, since=None, limit=None):
        """
        We define call so you can pass args like 'since' and 'limit' to the
        collection through methods like all()
        """
        # self.query_params = query_params or {}
        self.limit = limit
        if since:
            self.query_params['since'] = since
        return self

    def __repr__(self):
        return object.__repr__(self) + (" of <%s>" % self.resource.__name__)

    def __iter__(self):
        return self

    def __len__(self):
        if self.limit:
            return min(self.size, self.limit)
        else:
            return self.size

    @property
    def size(self):
        if not self.current_page_num:
            self._load_page(0)
        return self._size

    def next(self):
        # load the first page if we haven't loaded anything yet
        if self.current_page_num is None:
            logging.debug("LOADING FIRST PAGE")
            self._load_page(0)

        # we hit the limit
        if self.limit and self.overall_position >= self.limit:
            raise StopIteration

        # we ran out of items
        if self.overall_position >= self.current_page_size:
            raise StopIteration

        # if we've already shown the last item on the page, get the next page
        if self.current_page_position >= self.current_page_size:
            logging.debug("LOADING NEXT PAGE (#%d)" % (self.current_page_num + 1))
            self._load_page(self.current_page_num + 1)

        # turn the raw data into a Resource
        item = self.resource._build(self.current_page_raw_items[self.current_page_position], is_snippet=False)

        # update indices
        self.overall_position += 1
        self.current_page_position += 1
        return item

    def _load_page(self, page_num):
        logging.debug("LOADING PAGE [%d]" % page_num)
        # reset the states
        self.current_page_num = page_num
        self.current_page_position = 0

        # get the page
        items, total, links = self.resource._request_paginated(self.resource.collection_url,
                                                               query_params=self.query_params,
                                                               page=page_num)

        # save some info
        self.current_page_size = len(items)
        self.current_page_raw_items = items
        self._size = total
