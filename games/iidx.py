import json5

from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def _parse_diff(full_diff: str) -> tuple[str, str]:
    mode = full_diff[:2]

    match full_diff[2]:
        case "B":
            return mode, "BEGINNER"
        case "N":
            return mode, "NORMAL"
        case "H":
            return mode, "HYPER"
        case "A":
            return mode, "ANOTHER"
        case "L":
            return mode, "LEGGENDARIA"


def _parse_graph_script(script: str) -> dict:
    start = script.find("= {") + 2
    end = script.find("};") + 1

    datasets = json5.loads(script[start:end])["datasets"]

    start = script.find("ticks: {", end) + 7
    end = script.find("}", start) + 1

    options = json5.loads(script[start:end])
    gauge = [data["y"] for data in datasets[0]["data"]]
    scores = [
        min(110, data) / 1.1 for data in datasets[1]["data"]
    ]  # max is 110 not 100 which tachi expects
    return {
        "score": scores,
        "gauge": (gauge + options["max"] * [None])[: options["max"]],
    }


def parse_iidx(songs: list[FlowerSongData], game: Game) -> dict:
    json_data = create_base(game.tachi_gpt)

    for song in songs:
        graph_data = _parse_graph_script(song.iidx_script)

        diff = _parse_diff(song.header[4].find("b").previous_sibling.text.strip())
        if diff == "BEGINNER":
            continue
        judgements = [None, None, None, None, None, None, None]  # fast slow at end

        if game.tachi_gpt[1] != diff[0]:
            continue
        try:
            j = song.accordion[2].find("small").text[1:-1].split()
            judgements[0] = int(j[0])
            judgements[1] = int(j[2])
        except AttributeError:
            for i in range(5):
                judgements[i] = int(song.accordion[i + 11].find("br").next_sibling.text)
            fast_slow = song.accordion[16].find("br").next_sibling.text.split(" / ")
            judgements[5] = int(fast_slow[0])
            judgements[6] = int(fast_slow[1])

        song_data = {
            "matchType": "inGameID",
            "identifier": song.url[7],
            "score": int(song.accordion[2].find("br").next_sibling.text.strip()),
            "lamp": song.header[5].find("strong").text,
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
                    0 if graph_data["gauge"][-1] is None else graph_data["gauge"][-1]
                ),
                "fast": judgements[5],
                "slow": judgements[6],
            },
        }
        json_data["scores"].append(song_data)
    return json_data
