from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config import FLOWER_SESSION


class FlowerSongData:
    def __init__(self, song_element: BeautifulSoup) -> None:
        self.url = song_element.find("a")["href"].split("/")
        self.header = song_element.find_all("td")
        accordion_div = song_element.parent.find("div", id=song_element["data-target"][1:])  # to remove padding div
        self.accordion = accordion_div.find("div", recursive=False).find_all("div", recursive=False)


def parse_page(url: str) -> list[FlowerSongData]:
    s = requests.Session()
    s.cookies.set("flower_session", FLOWER_SESSION)
    res = s.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    songs: list[FlowerSongData] = list[FlowerSongData]()  # huh type checking complains if you use []
    song_row = soup.find_all("tr", class_="accordion-toggle")

    for song in song_row:
        songs.append(FlowerSongData(song))
    return songs


def parse_date(date_str: str) -> int:
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
