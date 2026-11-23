from typing import Literal

# needed for easy parsing of the data in JS scripts which flower generates graphs from
import pyjson5 as json5

from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def _parse_diff(full_diff: str) -> tuple[str, str]:
    mode = full_diff[:2]
    diff_map = {
        "B": "BEGINNER",
        "N": "NORMAL",
        "H": "HYPER",
        "A": "ANOTHER",
        "L": "LEGGENDARIA",
    }
    return mode, diff_map[full_diff[2]]


def _parse_graph_script(script: str) -> dict:
    start = script.find("data = {") + 7
    end = script.find("};", start) + 1
    datasets = json5.loads(script[start:end])["datasets"]

    start = script.find("options = {", end) + 10
    end = script.find("};", start) + 1
    # options now has a callback fn in it, sanitize it out
    options_script = script[start:end]
    cb_start = options_script.find("function(")
    cb_end = options_script.find("}", cb_start) + 1 # hacky, only works if there's no nested blocks in the fn
    options_script = options_script[:cb_start] + "0" + options_script[cb_end:]
    print(options_script)

    options = json5.loads(options_script)
    y_options = options["scales"]["y"]

    gauge = [min(100, data["y"]) for data in datasets[0]["data"]]
    scores = [min(100, data) for data in datasets[1]["data"]]
    return {
        "score": scores,
        "gauge": (gauge + y_options["max"] * [None])[: y_options["max"]],
    }


class IIDX(Game):
    def __init__(self, playtype: Literal["SP", "DP"]):
        super().__init__("beatmania IIDX", ("iidx", playtype))

    def parse(self, songs: list[FlowerSongData]) -> dict:
        json_data = create_base(self.tachi_gpt)

        for song in songs:
            if (
                len(song.url) != 9
            ):  # ignore url that isnt a song, weekly stuff shows as link like this
                continue

            diff = _parse_diff(song.header[4].find("b").previous_sibling.text.strip())
            if diff == "BEGINNER":
                continue

            lamp = song.header[5].find("strong").text
            if lamp == "EX-HARD CLEAR":
                lamp = "EX HARD CLEAR"

            if self.tachi_gpt[1] != diff[0]:
                continue

            graph_data = _parse_graph_script(song.iidx_script)
            judgements = [None, None, None, None, None, None, None]  # fast slow at end

            try:
                j = song.accordion[2].find("small").text[1:-1].split()
                judgements[0] = int(j[0])
                judgements[1] = int(j[2])
            except AttributeError:
                for i in range(5):
                    judgements[i] = int(
                        song.accordion[i + 11].find("br").next_sibling.text
                    )
                fast_slow = song.accordion[16].find("br").next_sibling.text.split(" / ")
                judgements[5] = int(fast_slow[0])
                judgements[6] = int(fast_slow[1])
            song_data = {
                "matchType": "inGameID",
                "identifier": song.url[7],
                "score": int(song.accordion[2].find("br").next_sibling.text.strip()),
                "lamp": lamp,
                "difficulty": diff[1],
                "timeAchieved": parse_date(song.header[8].find("small").text),
                "judgements": {
                    "pgreat": judgements[0],
                    "great": judgements[1],
                    "good": judgements[2],
                    "bad": judgements[3],
                    "poor": judgements[4],
                },
                "optional": {
                    "gaugeHistory": graph_data["gauge"],
                    "scoreHistory": graph_data["score"],
                    "gauge": (
                        0
                        if graph_data["gauge"][-1] is None
                        else graph_data["gauge"][-1]
                    ),
                    "fast": judgements[5],
                    "slow": judgements[6],
                },
            }
            json_data["scores"].append(song_data)
        return json_data
