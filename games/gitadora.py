from typing import Literal

from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


class Gitadora(Game):
    def __init__(self, playtype: Literal["Gita", "Dora"]):
        super().__init__("GITADORA", ("gitadora", playtype))

    def parse(self, songs: list[FlowerSongData]) -> dict:
        json_data = create_base(self.tachi_gpt)

        for song in songs:
            mode = song.url[8]
            # 0 = drum, 1 = guitar, 2 = bass for if i ever forget
            wrong_mode = (
                (mode == "1" or mode == "2")
                if self.tachi_gpt[1] == "Dora"
                else (mode == "0")
            )
            if wrong_mode:
                continue

            diff_prefix = "BASS " if mode == "2" else ""
            song_data = {
                "matchType": "inGameID",
                "identifier": song.url[7],
                "percent": float(song.header[4].find("small").text.strip()[:-1]),
                "lamp": song.header[5].find("strong").text.strip().upper(),
                "difficulty": diff_prefix
                + (song.header[2].find("strong").next_sibling.text.strip().upper()),
                "timeAchieved": parse_date(song.header[6].find("small").text),
                "judgements": {
                    "perfect": int(song.accordion[4].find("br").next_sibling.text),
                    "great": int(song.accordion[5].find("br").next_sibling.text),
                    "good": int(song.accordion[6].find("br").next_sibling.text),
                    "ok": int(song.accordion[7].find("br").next_sibling.text),
                    "miss": int(song.accordion[8].find("br").next_sibling.text),
                },
                "optional": {
                    "maxCombo": int(song.accordion[9].find("br").next_sibling.text)
                },
            }
            json_data["scores"].append(song_data)
        return json_data
