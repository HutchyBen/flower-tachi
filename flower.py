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


# This now stores the home page so a request isnt made for every single playtype
def find_profile_url(game: Game):
    if find_profile_url.home_page is None:
        find_profile_url.home_page = flower_get("https://projectflower.eu")

    button = find_profile_url.home_page.find("a", attrs={"title": game.flower_name})
    if button is None:
        raise Exception("Game not found on your profile")
    return button["href"]


find_profile_url.home_page = None


def _should_score_exist(score: FlowerSongData, date: datetime) -> bool:
    recent_song = score.header[-1].find("small").text
    recent_date = datetime.strptime(recent_song, "%Y-%m-%d %I:%M %p")
    return recent_date <= date


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
        index += 1
    return songs


def iter_pages(start_url):
    url = start_url
    while url is not None:
        if url in iter_pages.page_cache:
            # page is cached
            yield iter_pages.page_cache[url][0]
            url = iter_pages.page_cache[url][1]
        else:
            # get current page and parse
            soup = flower_get(url)
            song_row = soup.find_all("tr", class_="accordion-toggle")
            if len(song_row) == 0:
                break
            parsed = _parse_page(song_row, soup, "iidx" in url)

            # get next url.
            paginator = soup.find("ul", class_="pagination")
            next_button = paginator.find_all("li")[-1].find("a") if paginator else None
            next_url = next_button["href"] if next_button else None

            iter_pages.page_cache[url] = (parsed, next_url)
            yield parsed
            url = next_url


iter_pages.page_cache = {}


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
            print("Could not find any sessions. Assuming all scores are needed")
            for page in iter_pages(url):
                songs.extend(page)
            return songs
        
        for page in iter_pages(url):
            songs.extend(page)
            if _should_score_exist(page[-1], date):
                break

        # filter out songs that should already be in tachi
        return list(filter(lambda x: not _should_score_exist(x, date), songs))

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
