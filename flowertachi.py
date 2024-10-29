import argparse
import json
from io import TextIOWrapper
from typing import List

from config import FLOWER_SESSION, TACHI_API_KEY
from flower import parse_pages
from ft_types import Game, Arguments
from games.ddr import DanceDanceRevolution
from games.gitadora import Gitadora
from games.iidx import IIDX
from games.jubeat import Jubeat
from games.museca import Museca
from games.popn import PopnMusic
from games.sound_voltex import SoundVoltex

from tachi import submit_score

SUPPORTED_GAMES: List[Game] = [
    DanceDanceRevolution("SP"),
    DanceDanceRevolution("DP"),
    PopnMusic(),
    Gitadora("Gita"),
    Gitadora("Dora"),
    Jubeat(),
    IIDX("SP"),
    IIDX("DP"),
    Museca(),
    SoundVoltex(),
]


def parse_numbers(nums_input: list[str]) -> list[int] | str:
    numbers = set()
    if not nums_input:
        return [1]

    for part in nums_input:
        try:
            if part == "all":
                return "all"
            elif part == "recent":
                return "recent"
            if "-" in part:
                start, end = map(int, part.split("-"))
                numbers.update(range(start, end + 1))
            else:
                numbers.add(int(part))
        except ValueError:
            print("Invalid number entered")
            exit(1)
    return sorted(numbers)


def handle_arguments() -> Arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g",
        "--games",
        nargs="+",
        choices=[f"{g.tachi_gpt[0]}:{g.tachi_gpt[1]}" for g in SUPPORTED_GAMES]
        + ["all"],
        help="Choose one or more games to import, or 'all' for all games",
        required=True,
    )
    parser.add_argument(
        "-p",
        "--pages",
        nargs="*",
        help='Choose pages to import, defaults to first page. "all" for all pages, "recent" for pages since last session (e.g. "1-5 7 9")',
    )
    parser.add_argument(
        "-j",
        "--json",
        action="store_true",
        help="Output JSON file instead of uploading to tachi",
    )
    parsed = parser.parse_args()
    if "all" in parsed.games:
        games = SUPPORTED_GAMES
    else:
        games = [
            g
            for g in SUPPORTED_GAMES
            if f"{g.tachi_gpt[0]}:{g.tachi_gpt[1]}" in parsed.games
        ]

    return Arguments(games, parse_numbers(parsed.pages), parsed.json)


if __name__ == "__main__":
    if FLOWER_SESSION == "":
        print("Flower session cookie is not provided. Aborting")
        exit(1)

    args = handle_arguments()

    if not args.json and TACHI_API_KEY == "":
        print(
            "TACHI_API_KEY is not present in config. Please use --json or provide an API KEY"
        )
        exit(1)

    # games with different playtypes come up in same list and dont wanna flood flower with requests
    page_cache = {}
    for game in args.games:
        if game.flower_name not in page_cache:
            page_data = parse_pages(game, args.pages)
            page_cache[game.flower_name] = page_data
        tachi_json = game.parse(page_cache[game.flower_name])
        if args.json:
            filename = f"score_{game.tachi_gpt[0]}_{game.tachi_gpt[1]}.json"
            with open(filename, "w") as f:  # type: TextIOWrapper
                print(
                    f"Writing {game.flower_name} ({game.tachi_gpt[1]}) scores to",
                    filename,
                )
                json.dump(tachi_json, f, indent=4)
        else:
            print(f"Uploading {game.flower_name} ({game.tachi_gpt[1]}) scores to tachi")
            submit_score(tachi_json)
