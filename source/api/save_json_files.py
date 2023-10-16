"""Save json utils module."""
from source.api.api_request_object import MagicApiRequest
from definitions import ROOT_DIR
import json


def save_json_files(magic_request_object: MagicApiRequest) -> None:
    """Save API request returned jsons.

    Args:
        magic_request_object (MagicApiRequest): MagicApiRequest object.
    """
    for magic_api in magic_request_object.json_list:
        file_name = f"{magic_request_object.endpoint.replace('https://','').replace('/', '_')}?page={magic_api['page']}.json"
        sub_dir_name = list(magic_api.keys())[0]
        with open(f"{ROOT_DIR}/data/tlz/{sub_dir_name}/{file_name}", "w", encoding='utf8') as json_file:
            json.dump(magic_api, json_file, ensure_ascii=False)
