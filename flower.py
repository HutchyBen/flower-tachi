from datetime import datetime

import requests
from bs4 import BeautifulSoup, ResultSet

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


def _parse_page(
    page_songs: ResultSet, page: BeautifulSoup, iidx: bool
) -> list[FlowerSongData]:
    index = 0
    songs: list[FlowerSongData] = list[FlowerSongData]()
    for song in page_songs:
        if iidx:
            script = page.find_all("script")[index + 4].text
        else:
            script = None
        songs.append(FlowerSongData(song, script))
    return songs


def parse_pages(url: str, pages: list[int]) -> list[FlowerSongData]:
    songs: list[FlowerSongData] = list[
        FlowerSongData
    ]()  # huh type checking complains if you use []

    for page in pages:
        soup = flower_get(f"{url}?page={page}")
        song_row = soup.find_all("tr", class_="accordion-toggle")
        if len(song_row) == 0:
            return songs
        songs.extend(_parse_page(song_row, soup, "iidx" in url))

    if len(pages) == 0:
        # I WANT DO WHILE
        soup = flower_get(url)
        song_row = soup.find_all("tr", class_="accordion-toggle")
        while len(song_row) > 0:
            songs.extend(_parse_page(song_row, soup, "iidx" in url))

            paginator = soup.find("ul", class_="pagination")
            if not paginator:
                return songs

            next_button = paginator.find_all("li")[-1].find("a")
            if not next_button:
                return songs

            soup = flower_get(next_button["href"])
            song_row = soup.find_all("tr", class_="accordion-toggle")

    return songs


def parse_date(date_str: str) -> int:
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
