import json
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

    def _request(self, url, query_params=None):
        """
        Requests a URL given the RestClient's options and the given query_params
        and returns the results parsed from JSON into a dict. An exception is raised
        if a non-ok HTTP error code.
        """
        logging.debug("GET [%s]" % url)

        request_options = self._request_options.copy()
        if query_params:
            request_options['params'].update(query_params)

        response = requests.get(url, **request_options)
        logging.debug(response.url)
        response.raise_for_status()
        return response.json()

    def _request_paginated(self, url, query_params=None, page=0, header_total_items_key='total'):
        """
        Requests a URL and specific page given the RestClient's options and the given
        query_params and returns a tuple of
            1) the results parsed from JSON into a dict
            2) the total number of items in the collection
            3) a dictionary of links to prev, next, first, last
        An exception is raised if a non-ok HTTP error code.
        """
        logging.debug("GET PAGE %d [%s]" % (page, url))

        request_options = self._request_options.copy()
        if query_params:
            request_options['params'].update(query_params)
        request_options['params']['page'] = page

        response = requests.get(url, **request_options)
        logging.debug(response.url)
        response.raise_for_status()

        return response.json(), int(response.headers[header_total_items_key]), response.links


class Resource(object):
    """
    A resource that can be retrieved through the API. Should be subclassed to define resources:

        class Animal(Resource):
            pass

    Then you can get all the animals:

        Animal(client).all()

    Or just one by ID:

        Animal(client).find(7)

    @param client A RestClient
    @param resource_path The REST path to get the resource from the server
                         (ie, 'https://foo.bar/api/<resource_path>). Defaults
                         to the class name pluralized Brian Regan style by adding an 's'.
    @param collection_url The URL to get the collection of Resources (the index route).
                          Can be overridden for nested resources.
    @param snippet_url_attribute The attribute name where the URL is found to get the
                                 full object.
    """
    client = None
    resource_path = None
    collection_url = None
    snippet_url_attribute = None

    def __init__(self, client, resource_path=None, collection_url=None, snippet_url_attribute='url'):
        """
        Creates a way to get the Resource via all() and find()
        """
        # print "New %s, client: %s, data: %s" % (self.__class__.__name__, client, data)
        Resource.client = client
        Resource.resource_path = resource_path or (self.__class__.__name__.lower() + 's')
        Resource.collection_url = collection_url or ("%s/%s" % (Resource.client.base_url, Resource.resource_path))
        Resource.snippet_url_attribute = snippet_url_attribute

    @classmethod
    def all(cls):
        """
        Returns an iterable PaginatedCollection for iterating through the collection of resources
        """
        return PaginatedCollection(cls)

    @classmethod
    def find(cls, id):
        """
        Finds a resource by ID
        """
        return cls.build(cls.client._request("%s/%d" % (cls.collection_url, id)), is_snippet=False)

    @classmethod
    def build(cls, data, is_snippet):
        """
        Builds an object from the JSON data received from the API
        """
        object = cls(cls.client)
        object._load_from_data(data, is_snippet)
        return object

    def has_many(self, klass, field_name, is_snippet=True):
        """
        Defines a has_many association of <klass> objects that is loaded from the <field_name> attribute
        """
        return list([klass.build(snippet, is_snippet=is_snippet) for snippet in self._data[field_name]])

    def has_one(self, klass, field_name, is_snippet=True):
        """
        Defines a has_one association of a <klass> object that is loaded from the <field_name> attribute
        """
        return klass.build(self._data[field_name], is_snippet=is_snippet)

    @property
    def as_json(self):
        return json.dumps(self._data)

    def __getattr__(self, name):
        """
        Gets a missing attribute in the following way:
        1) if the attribute is a key in the 'data dict received from the server, return the value
        2) if our current Resource is a "snippet" (a partially filled in Resource missing some fields),
            request the full resource from the server and fill in our Resource with the data, then
            call getattr again to get the attribute's value
        """
        if name in self._data:
            return self._data[name]
        elif self._is_snippet:
            # we are only a snippet, so we need to get the full object info
            self._load_from_data(self.client._request(self.url), is_snippet=False)
            # and then get the attribute again
            return self.__getattr__(name)
        else:
            raise AttributeError("No such attribute: " + name)

    def _load_from_data(self, data, is_snippet=False):
        """
        Loads the given data into this resource and flags if this is a snippet or full object
        """
        self.__setattr__('_data', data)
        self.__setattr__('_is_snippet', is_snippet)

    def __repr__(self):
        return object.__repr__(self) + ":" + self._data.__repr__()


class PaginatedCollection(object):
    """
    An iterable collection of Resources that supports server-side pagination. Keep iterating
    over this object and it will request new pages from the server as needed.

    len(<collection>) returns the number of items in the collection (affected by limit=)

    <collection>.size returns the total number of items on the server

    'Call' the collection to pass in 'limit' and 'since' query params. This is done with __call__
    so a PaginatedCollection can be returned from a @property but given kwargs (limit, since, etc)
    like a method:

        MyResource.all(limit=10)
    """

    def __init__(self, resource):
        self.resource = resource

        # set the states
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
        """
        The total number of items in the collection as reported by the server (not affected by limit=)
        """
        if not self.current_page_num:
            self._load_page(1)
        return self._size

    def next(self):
        # load the first page if we haven't loaded anything yet
        if self.current_page_num is None:
            logging.debug("LOADING FIRST PAGE")
            self._load_page(1)

        # we hit the limit
        if self.limit and self.overall_position >= self.limit:
            raise StopIteration

        # we ran out of items
        if self.overall_position >= self._size:
            raise StopIteration

        # if we've already shown the last item on the page, get the next page
        if self.current_page_position >= self.current_page_size:
            logging.debug("LOADING NEXT PAGE (#%d)" % (self.current_page_num + 1))
            self._load_page(self.current_page_num + 1)

        # turn the raw data into a Resource
        item = self.resource.build(self.current_page_raw_items[self.current_page_position], is_snippet=False)

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
        items, total, links = self.resource.client._request_paginated(self.resource.collection_url,
                                                                      query_params=self.query_params,
                                                                      page=page_num)

        # save some info
        self.current_page_size = len(items)
        self.current_page_raw_items = items
        self._size = total
