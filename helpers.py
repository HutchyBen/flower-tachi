from datetime import datetime


def create_base(game, playtype):
    return {
        "meta": {
            "game": game,
            "playtype": playtype,
            "service": "flower-tachi"
        },
        "scores": []
    }


def parse_date(date_str):
    date_format = "%Y-%m-%d %I:%M %p"
    date = datetime.strptime(date_str, date_format)
    return int(date.timestamp() * 1000)
