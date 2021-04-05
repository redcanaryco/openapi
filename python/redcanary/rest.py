import requests
import logging 

class RestClient(object):
    """
    Class for interacting with the Rest API 
    
    """

    def __init__(self, customer_id: str, auth_key: str):
        """
        Parameters
        --------
        url : str
            full url to API 
        params : dict
            dictionary of params passed in query
            must contain the auth token
        """
        self._baseurl = f"https://{customer_id}.my.redcanary.co/openapi/v3/"
        self._headers = dict({
            'X-Api-Key': auth_key
            })
    
    @property 
    def baseurl(self) -> str:
        return self._baseurl
    
    @property
    def headers(self) -> dict:
        return self._headers

    def _get_all(self, api_path: str, params: dict) -> list:
        """returns list of all items returned by API query"""
        setattr(self, 'params', params)
        
        return self._paginated_requests(self._baseurl + api_path, params)

    def _paginated_requests(self, url: str, params: dict) -> list:
        """
        Iterates through API until all items queried 
        sets length property 
        return list of items from data field in API response
        """
        params.update({'page' : 1})
        ret_item_list = []

        first_page = requests.get(url, headers=self._headers, params=params)
        first_page.raise_for_status()
        total_items_int = first_page.json().get('meta').get('total_items')
        setattr(self, 'total', total_items_int)
        ret_item_list.extend(first_page.json().get('data'))

        while len(ret_item_list) != total_items_int:
            params['page'] += 1
            next_page = requests.get(url, headers=self._headers, params=params).json()
            ret_item_list.extend(next_page.get('data'))

        return ret_item_list 
