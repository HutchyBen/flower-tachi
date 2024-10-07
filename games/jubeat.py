from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def parse_jubeat(songs: list[FlowerSongData], game: Game) -> dict:
    json_data = create_base(game.tachi_gpt)
    for song in songs:
        is_hard = song.header[2].find("span", class_="hidden-xs") is not None

        judgements = [0, 0, 0, 0, 0]
        if len(song.accordion) > 7:
            for i in range(0, 5):
                judgements[i] = int(song.accordion[i + 7].find("br").next_sibling.text)

        song_data = {
            "matchType": "inGameID",
            "identifier": song.url[7],
            "score": int(song.header[3].find("small").text.strip()),
            "musicRate": float(song.header[4].find("strong").text.strip()[:-1]),
            "lamp": song.header[5].find("strong").text.upper(),
            "difficulty": ("HARD " if is_hard else "")
            + song.header[2].find("strong").previous_sibling.text.strip(),
            "timeAchieved": parse_date(song.header[7].find("small").text),
            "judgements": {
                "perfect": judgements[0],
                "great": judgements[1],
                "good": judgements[2],
                "poor": judgements[3],
                "miss": judgements[4],
            },
            "optional": {
                "musicBar": list(
                    map(float, song.accordion[0]["data-jubeat-judge"].split(" "))
                )
            },
        }
        json_data["scores"].append(song_data)
    return json_data
