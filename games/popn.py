from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base

# padding out by one
medals = [
    "lazycoding",
    "failedCircle",
    "failedDiamond",
    "failedStar",
    "easyClear",
    "clearCircle",
    "clearDiamond",
    "clearStar",
    "fullComboCircle",
    "fullComboDiamond",
    "fullComboStar",
    "perfect",
]


def parse_popn(songs: list[FlowerSongData], game: Game) -> dict:
    json_data = create_base(game.tachi_gpt)
    for song in songs:
        diff_name = song.header[1].find("br").next_sibling.text.strip()
        if diff_name != "EX":
            diff_name = diff_name.capitalize()
        song_data = {
            "matchType": "inGameID",
            "identifier": song.url[7],
            "score": int(song.header[3].find("div").text.strip()),
            "clearMedal": medals[
                int(song.header[2].find("img")["src"].split("_")[-1][:-4])
            ],
            "difficulty": diff_name,
            "timeAchieved": parse_date(song.header[5].find("small").text),
            "judgements": {
                "cool": int(song.accordion[5].find("br").next_sibling.text),
                "great": int(song.accordion[6].find("br").next_sibling.text),
                "good": int(song.accordion[7].find("br").next_sibling.text),
                "bad": int(song.accordion[8].find("br").next_sibling.text),
            },
        }
        json_data["scores"].append(song_data)
    return json_data
