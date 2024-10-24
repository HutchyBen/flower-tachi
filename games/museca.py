from flower import parse_date
from ft_types import Game, FlowerSongData
from tachi import create_base


def parse_museca(songs: list[FlowerSongData], game: Game) -> dict:
    json_data = create_base(game.tachi_gpt)

    for song in songs:
        diff = ""
        score = int(song.header[3].find("strong").text.strip().replace(",", ""))
        match song.header[2].find("b").previous_sibling.text.strip():
            case "朱":
                diff = "Red"
            case "橙":
                diff = "Yellow"
            case "翠":
                diff = "Green"

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
                "critical": int(song.accordion[1].find("br").next_sibling.text.strip()),
                "near": int(song.accordion[2].find("br").next_sibling.text.strip()),
                "miss": int(song.accordion[3].find("br").next_sibling.text.strip()),
            },
        }
        json_data["scores"].append(song_data)
    return json_data
