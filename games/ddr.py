from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def _get_difficulty_name(difficulty: int) -> str:
    match difficulty:
        case 0:
            return "BEGINNER"
        case 1 | 5:
            return "BASIC"
        case 2 | 6:
            return "DIFFICULT"
        case 3 | 7:
            return "EXPERT"
        case 4 | 8:
            return "CHALLENGE"


def parse_ddr(songs: list[FlowerSongData], game: Game) -> dict:
    json_data = create_base(game.tachi_gpt)
    json_data["meta"]["version"] = "a3"
    for song in songs:
        diff = int(song.url[8])
        if game.tachi_gpt[1] == "SP" and diff >= 5:
            continue
        if game.tachi_gpt[1] == "DP" and diff < 5:
            continue

        grade = song.header[4].find("strong").text
        lamp = "FAILED" if grade == "E" else "CLEAR"  # TOOO: not sure how to handle assist or life4 yet
        clear_type = song.header[5].find("small")
        if clear_type:
            lamp = clear_type["title"]
            # different names in tachi
            if lamp == "EXTRA CLEAR":  # this is an assumption
                lamp = "LIFE4"
            elif lamp == "GOOD FULL COMBO":
                lamp = "FULL COMBO"

        song_data = {
            "matchType": "inGameID",
            "identifier": song.url[7],
            "score": int(song.header[3].find("strong").text.strip().replace(",", "")),
            "lamp": lamp,
            "difficulty": _get_difficulty_name(diff),
            "timeAchieved": parse_date(song.header[8].find("small").text),
            "judgements": {
                "MARVELOUS": int(song.accordion[6].find_all("div")[0].find("br").next_sibling.text.strip()),
                "PERFECT": int(song.accordion[6].find_all("div")[1].find("br").next_sibling.text.strip()),
                "GREAT": int(song.accordion[6].find_all("div")[2].find("br").next_sibling.text.strip()),
                "GOOD": int(song.accordion[6].find_all("div")[3].find("br").next_sibling.text.strip()),
                "MISS": int(song.accordion[6].find_all("div")[5].find("br").next_sibling.text.strip()) + int(
                    song.accordion[6].find_all("div")[6].find("br").next_sibling.text.strip()),
                "OK": int(song.accordion[6].find_all("div")[4].find("br").next_sibling.text.strip()),
            },
        }
        json_data["scores"].append(song_data)
    return json_data
