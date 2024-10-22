from datetime import datetime

import requests
from bs4 import BeautifulSoup, ResultSet

from config import FLOWER_SESSION
from ft_types import FlowerSongData, Game
from tachi import get_recent_session


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


class iter_pages(object):
    def __init__(self, start_url):
        self.url = start_url
        self.soup = None

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        if self.soup is not None:
            paginator = self.soup.find("ul", class_="pagination")
            if not paginator:
                raise StopIteration()

            next_button = paginator.find_all("li")[-1].find("a")
            if not next_button:
                raise StopIteration()
            self.url = next_button["href"]

        self.soup = flower_get(self.url)
        song_row = self.soup.find_all("tr", class_="accordion-toggle")
        if len(song_row) == 0:
            raise StopIteration()

        return _parse_page(song_row, self.soup, "iidx" in self.url)


def parse_pages(game: Game, pages: list[int]) -> list[FlowerSongData]:
    url = find_profile_url(game)

    songs: list[FlowerSongData] = list[
        FlowerSongData
    ]()  # huh type checking complains if you use []

    if pages == "all":
        for page in iter_pages(url):
            songs.extend(page)
        return songs

    if pages == "recent":
        date: datetime.date
        try:
            session = get_recent_session(game.tachi_gpt)
            date = datetime.fromtimestamp(
                session["body"]["session"]["timeEnded"] / 1000
            )
        except RuntimeError:
            print("Could not find any sessions. Aborting")
            exit(1)
        for page in iter_pages(url):
            songs.extend(page)

            oldest_song = songs[-1].header[-1].find("small").text
            oldest_date = datetime.strptime(oldest_song, "%Y-%m-%d %I:%M %p")
            if oldest_date < date:
                return songs

    for page in pages:
        soup = flower_get(f"{url}?page={page}")
        song_row = soup.find_all("tr", class_="accordion-toggle")
        if len(song_row) == 0:
            return songs
        songs.extend(_parse_page(song_row, soup, "iidx" in url))
    return songs


def parse_date(date_str: str) -> int:
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
