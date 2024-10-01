from helpers import create_base, parse_date


def parse_dora(soup):
    json_data = create_base("gitadora", "Dora")

    song_row = soup.find_all("tr", class_="accordion-toggle")
    for song in song_row:
        url = song.find("a")["href"].split("/")
        if url[8] != "0":  # ignore non drum modes
            continue

        extra_data = soup.find("div", id=song["data-target"][1:]).find("div", recursive=False).find_all("div",
                                                                                                        recursive=False)
        rows = song.find_all("td")

        song_data = {
            "matchType": "inGameID",
            "identifier": url[7],
            "percent": float(rows[4].find("small").text.strip()[:-1]),
            "lamp": rows[5].find("strong").text.strip().upper(),
            "difficulty": rows[2].find("strong").next_sibling.text.strip().upper(),
            "timeAchieved": parse_date(rows[6].find("small").text),
            "judgements": {
                "perfect": int(extra_data[4].find("br").next_sibling.text),
                "great": int(extra_data[5].find("br").next_sibling.text),
                "good": int(extra_data[6].find("br").next_sibling.text),
                "ok": int(extra_data[7].find("br").next_sibling.text),
                "miss": int(extra_data[8].find("br").next_sibling.text)
            },
            "optional": {
                "maxCombo": int(extra_data[9].find("br").next_sibling.text)
            }
        }
        json_data["scores"].append(song_data)
    return json_data
