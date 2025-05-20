from typing import Literal

from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base

FLARE_TEXT = ["0", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "EX"]


class DanceDanceRevolution(Game):
    def __init__(self, playtype: Literal["SP", "DP"]):
        super().__init__("DanceDanceRevolution", ("ddr", playtype))

    def parse(self, songs: list[FlowerSongData]) -> dict:
        json_data = create_base(self.tachi_gpt)
        for song in songs:
            diff = song.header[2].find("br").previous_sibling.text.strip().split()
            if self.tachi_gpt[1] != diff[0]:
                continue

            grade = song.header[4].find("strong").text
            lamp = (
                "FAILED" if grade == "E" else "CLEAR"
            )  # TOOO: not sure how to handle assist or life4 yet
            clear_type = song.header[5].find("small")
            if clear_type:
                lamp = clear_type["title"]
                # different names in tachi
                if lamp == "EXTRA CLEAR":  # this is an assumption
                    lamp = "LIFE4"
                elif lamp == "GOOD FULL COMBO":
                    lamp = "FULL COMBO"
                elif lamp == "ASSIST CLEAR":
                    lamp = "ASSIST"

            flare_str = song.header[6].find("strong").text.strip()
            if len(song.accordion) == 7:
                judgements = {
                    "MARVELOUS": int(
                        song.accordion[6]
                        .find_all("div")[0]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                    "PERFECT": int(
                        song.accordion[6]
                        .find_all("div")[1]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                    "GREAT": int(
                        song.accordion[6]
                        .find_all("div")[2]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                    "GOOD": int(
                        song.accordion[6]
                        .find_all("div")[3]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                    "MISS": int(
                        song.accordion[6]
                        .find_all("div")[5]
                        .find("br")
                        .next_sibling.text.strip()
                    )
                    + int(
                        song.accordion[6]
                        .find_all("div")[6]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                    "OK": int(
                        song.accordion[6]
                        .find_all("div")[4]
                        .find("br")
                        .next_sibling.text.strip()
                    ),
                }
            else:
                judgements = {}

            song_data = {
                "matchType": "inGameID",
                "identifier": song.url[7],
                "score": int(
                    song.header[3].find("strong").text.strip().replace(",", "")
                ),
                "lamp": lamp,
                "difficulty": diff[1],
                "timeAchieved": parse_date(song.header[8].find("small").text),
                "judgements": judgements,
                "optional": {
                    "flare": FLARE_TEXT[int(flare_str)] if flare_str != "" else "0",
                },
            }
            json_data["scores"].append(song_data)
        return json_data
