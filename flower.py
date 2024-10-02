from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config import FLOWER_SESSION
from ft_types import FlowerSongData, Game


def flower_get(url: str) -> BeautifulSoup:
    s = requests.Session()
    s.cookies.set("flower_session", FLOWER_SESSION)
    res = s.get(url)
    return BeautifulSoup(res.text, "html.parser")


def find_profile_url(game: Game):
    soup = flower_get("https://projectflower.eu")
    button = soup.find("a", attrs={"title": game.flower_name})
    if button is None:
        raise Exception("Game not found on your profile")
    return button["href"]


def parse_page(url: str) -> list[FlowerSongData]:
    soup = flower_get(url)
    songs: list[FlowerSongData] = list[FlowerSongData]()  # huh type checking complains if you use []
    song_row = soup.find_all("tr", class_="accordion-toggle")

    for song in song_row:
        songs.append(FlowerSongData(song))

    paginator = soup.find("ul", class_="pagination")
    if paginator:
        next_button = paginator.find_all("li")[-1].find("a")
        if next_button:
            songs.extend(parse_page(next_button["href"]))

    return songs


def parse_date(date_str: str) -> int:
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
