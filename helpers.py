from datetime import datetime

from bs4 import BeautifulSoup


class FlowerSongData:
    def __init__(self, song_element: BeautifulSoup) -> None:
        self.url = song_element.find("a")["href"].split("/")
        self.header = song_element.find_all("td")
        accordion_div = song_element.parent.find("div", id=song_element["data-target"][1:])  # to remove padding div
        self.accordion = accordion_div.find("div", recursive=False).find_all("div", recursive=False)


def create_base(game: str, playtype: str) -> dict:
    return {
        "meta": {
            "game": game,
            "playtype": playtype,
            "service": "flower-tachi"
        },
        "scores": []
    }


def parse_date(date_str: str) -> int:
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
