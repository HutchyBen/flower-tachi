from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def _parse_diff(diff_str: str) -> str:
    diff_map = {
        "朱": "Red",
        "橙": "Yellow",
        "翠": "Green",
    }
    return diff_map[diff_str]


class Museca(Game):
    def __init__(self):
        super().__init__("MÚSECA", ("museca", "Single"))

    def parse(self, songs: list[FlowerSongData]) -> dict:
        json_data = create_base(self.tachi_gpt)

        for song in songs:
            score = int(song.header[3].find("strong").text.strip().replace(",", ""))

            diff = _parse_diff(song.header[2].find("b").previous_sibling.text.strip())
            lamp = song.header[5].find("strong").text.strip()

            # convert flower name to tachi
            if lamp == "CLEARED":
                lamp = "CLEAR"

            # in tachi scores much alays follow 800k is always clear
            if score < 800000:
                lamp = "FAILED"
            elif lamp == "FAILED":
                lamp = "CLEAR"

            song_data = {
                "matchType": "inGameID",
                "identifier": song.url[7],
                "score": score,
                "lamp": lamp,
                "difficulty": diff,
                "timeAchieved": parse_date(song.header[7].find("small").text),
                "judgements": {
                    "critical": int(
                        song.accordion[1].find("br").next_sibling.text.strip()
                    ),
                    "near": int(song.accordion[2].find("br").next_sibling.text.strip()),
                    "miss": int(song.accordion[3].find("br").next_sibling.text.strip()),
                },
            }
            json_data["scores"].append(song_data)
        return json_data
