import requests
from requests import Response

from config import TACHI_BASE_URL, TACHI_API_KEY, TACHI_IMPORT_ENDPOINT


def create_base(game: str, playtype: str) -> dict:
    return {
        "meta": {
            "game": game,
            "playtype": playtype,
            "service": "flower-tachi"
        },
        "scores": []
    }


def submit_score(json_data: dict) -> Response:
    headers = {"Authorization": "Bearer " + TACHI_API_KEY}
    return requests.post(TACHI_BASE_URL + TACHI_IMPORT_ENDPOINT, json=json_data, headers=headers)
