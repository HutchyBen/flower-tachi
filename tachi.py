from datetime import datetime

import requests
from requests import Response

from config import (
    TACHI_BASE_URL,
    TACHI_API_KEY,
    TACHI_IMPORT_ENDPOINT,
    TACHI_LATEST_SESSION_ENDPOINT,
)


def create_base(gpt: tuple[str, str]) -> dict:
    return {
        "meta": {"game": gpt[0], "playtype": gpt[1], "service": "flower-tachi"},
        "scores": [],
    }


def submit_score(json_data: dict) -> Response:
    headers = {"Authorization": "Bearer " + TACHI_API_KEY}
    return requests.post(
        TACHI_BASE_URL + TACHI_IMPORT_ENDPOINT, json=json_data, headers=headers
    )


def get_recent_session(ugpt: tuple[str, str]) -> datetime.date:
    headers = {"Authorization": "Bearer " + TACHI_API_KEY}
    res = requests.get(
        TACHI_BASE_URL + TACHI_LATEST_SESSION_ENDPOINT.format("me", ugpt[0], ugpt[1]),
        headers=headers,
    )
    if res.status_code != 200:
        raise RuntimeWarning("no session found")
    return res.json()
