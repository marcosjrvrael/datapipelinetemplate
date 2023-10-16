"""MagicApiRequest object module."""
import requests
import json


class MagicApiRequest:
    """MagicApiRequest class."""
    def __init__(self, endpoint: str, page_limit: int = 1):
        """Init method of MagicApiRequest class."""
        self.__endpoint = endpoint
        self.__page_limit = page_limit
        self.__json_list = self.generate_json_list()
        self.__headers = self.get_endpoint_headers()
        self.__total_pages = self.get_total_pages()

    @property
    def endpoint(self) -> str:
        """Endpoint property."""
        return self.__endpoint

    @endpoint.setter
    def endpoint(self, endpoint: str) -> 'endpoint':
        """Endpoint setter."""
        self.__endpoint = endpoint

    @property
    def page_limit(self) -> int:
        """Page Limit property."""
        return self.__page_limit

    @page_limit.setter
    def page_limit(self, page_limit: int) -> 'page_limit':
        """Page Limit setter."""
        self.__page_limit = page_limit

    @property
    def json_list(self) -> list:
        """Json List property."""
        return self.__json_list

    @property
    def headers(self) -> requests.structures.CaseInsensitiveDict:
        """Headers property."""
        return self.__headers

    @property
    def total_pages(self) -> int:
        """Total Pages property."""
        return self.__total_pages

    def get_endpoint_headers(self) -> requests.structures.CaseInsensitiveDict:
        """Get endpoint headers.

        Returns:
            requests.structures.CaseInsensitiveDict: Request headers.
        """
        request = requests.get(self.__endpoint)
        return request.headers

    def generate_json_list(self) -> list:
        """Generate a list of json with api return.

        Returns:
            list_jsons (list): List with api returning json.
        """
        list_jsons = []
        for page in range(self.__page_limit):
            url = f"{self.__endpoint}?page={page+1}"
            request = requests.get(url)
            request_dict = json.loads(request.content)
            request_dict.update({'page': page+1})
            list_jsons.append(request_dict)
        return list_jsons

    def get_total_pages(self) -> int:
        """Determine the maximum pages.

        Returns:
            (int): value of total pages.
        """
        return int(self.__headers['Total-Count']) // int(self.__headers['Page-Size'])


if __name__ == '__main__':
    api_request = MagicApiRequest('https://api.magicthegathering.io/v1/cards', 3)
    print(api_request.endpoint)
    print(api_request.headers)
    print(api_request.page_limit)
    print(api_request.total_pages)
    print(len(api_request.json_list))
    print(api_request.json_list[0].keys())
