from flower import parse_date, FlowerSongData
from tachi import create_base


def _parse_gitadora(songs: list[FlowerSongData], dora: bool, ) -> dict:
    json_data = create_base("gitadora", "Dora" if dora else "Gita")

    for song in songs:
        mode = song.url[8]
        # 0 = drum, 1 = guitar, 2 = bass for if i ever forget
        wrong_mode = (mode == "1" or mode == "2") if dora else (mode == "0")
        if wrong_mode:
            continue

        diff_prefix = "BASS " if mode == "2" else ""
        song_data = {
            "matchType": "inGameID",
            "identifier": song.url[7],
            "percent": float(song.header[4].find("small").text.strip()[:-1]),
            "lamp": song.header[5].find("strong").text.strip().upper(),
            "difficulty": diff_prefix + (song.header[2].find("strong").next_sibling.text.strip().upper()),
            "timeAchieved": parse_date(song.header[6].find("small").text),
            "judgements": {
                "perfect": int(song.accordion[4].find("br").next_sibling.text),
                "great": int(song.accordion[5].find("br").next_sibling.text),
                "good": int(song.accordion[6].find("br").next_sibling.text),
                "ok": int(song.accordion[7].find("br").next_sibling.text),
                "miss": int(song.accordion[8].find("br").next_sibling.text)
            },
            "optional": {
                "maxCombo": int(song.accordion[9].find("br").next_sibling.text)
            }
        }
        json_data["scores"].append(song_data)
    return json_data


def parse_dora(songs: list[FlowerSongData]) -> dict:
    return _parse_gitadora(songs, True)


def parse_gitabass(songs: list[FlowerSongData]) -> dict:
    return _parse_gitadora(songs, False)
