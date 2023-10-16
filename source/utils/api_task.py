"""Api task module."""
from source.api.api_request_object import MagicApiRequest
from source.api.save_json_files import save_json_files

VALID_URLS = [
    'https://api.magicthegathering.io/v1/cards',
    'https://api.magicthegathering.io/v1/sets'
]


def run_api_task(api_task: str, api_url: str, page_limit: int) -> None:
    """Create an api request and save the return.

    Args:
        api_task (str): Type of api request (sets or cards).
        api_url (str): Endpoin url.
        page_limit (int): Limit of pages to be collected,
                          cannot override API own limit.

    Raises:
        ValueError: For invalid urls.
    """
    if api_task == 'sets':
        page_limit = 1

    if api_url in VALID_URLS:
        api_req = MagicApiRequest(api_url, page_limit)
        save_json_files(api_req)
    else:
        raise ValueError(f"Invalid url {api_url}")
