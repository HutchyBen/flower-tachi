from typing import List
from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class FlowerSongData:
    def __init__(self, song_element: BeautifulSoup, iidx_script: str) -> None:
        self.url = song_element.find("a")["href"].split("/")
        self.header = song_element.find_all("td")
        accordion_div = song_element.parent.find(
            "div", id=song_element["data-target"][1:]
        )  # to remove padding div
        self.accordion = accordion_div.find("div", recursive=False).find_all(
            "div", recursive=False
        )
        self.iidx_script = iidx_script


class Game(ABC):
    def __init__(
        self,
        flower_name: str,
        tachi_gpt: tuple[str, str],
    ) -> None:
        """
        Represents all the names a game can go by
        :param flower_name: Friendly name used by buttons. User-friendly name and used for scraping
        :param tachi_gpt: Name used internally by tachi to identify games + playtype. Playtype is used for display name
        """
        self.flower_name = flower_name
        self.tachi_gpt = tachi_gpt

    @abstractmethod
    def parse(self, songs: list[FlowerSongData]) -> dict:
        pass


class Arguments(object):
    def __init__(self, games: List[Game], pages: List[int], json: bool):
        self.games = games
        self.pages = pages
        self.json = json
