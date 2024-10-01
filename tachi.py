import requests
from requests import Response

from config import TACHI_BASE_URL, TACHI_API_KEY, TACHI_IMPORT_ENDPOINT


def submit_score(json_data: dict) -> Response:
    headers = {"Authorization": "Bearer " + TACHI_API_KEY}
    return requests.post(TACHI_BASE_URL + TACHI_IMPORT_ENDPOINT, json=json_data, headers=headers)
