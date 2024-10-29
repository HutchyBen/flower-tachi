from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


class SoundVoltex(Game):
    def __init__(self):
        super().__init__("Sound Voltex", ("sdvx", "Single"))

    def parse(self, songs: list[FlowerSongData]) -> dict:
        json_data = create_base(self.tachi_gpt)

        for song in songs:
            lamp = song.header[3].find("strong").text.strip()
            if lamp == "PLAYED":
                lamp = "FAILED"
            elif lamp == "HARD CLEAR":
                lamp = "EXCESSIVE CLEAR"

            fast_slow = (
                song.accordion[14].find("br").next_sibling.text.strip().split(" / ")
            )
            song_data = {
                "matchType": "sdvxInGameID",
                "identifier": song.url[7],
                "score": int(song.header[5].text.strip().replace(",", "")),
                "lamp": lamp,
                "difficulty": song.header[2].find("b").previous_sibling.text.strip(),
                "timeAchieved": parse_date(song.header[7].find("small").text),
                "judgements": {
                    "critical": int(
                        song.accordion[8].find("br").next_sibling.text.strip()
                    ),
                    "near": int(song.accordion[9].find("br").next_sibling.text.strip()),
                    "miss": int(
                        song.accordion[10].find("br").next_sibling.text.strip()
                    ),
                },
                "optional": {
                    "fast": int(fast_slow[0]),
                    "slow": int(fast_slow[1]),
                    "maxCombo": int(
                        song.accordion[6].find("br").next_sibling.text.strip()
                    ),
                },
            }
            json_data["scores"].append(song_data)
        return json_data
