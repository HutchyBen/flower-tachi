import argparse
import json

from config import FLOWER_SESSION, TACHI_API_KEY
from flower import find_profile_url, parse_page
from ft_types import Game
from games.ddr import parse_ddr
from games.gitadora import parse_gitadora
from games.jubeat import parse_jubeat
from games.popn import parse_popn
from tachi import submit_score

SUPPORTED_GAMES = [
    Game("DanceDanceRevolution", ("ddr", "SP"), parse_ddr),
    Game("DanceDanceRevolution", ("ddr", "DP"), parse_ddr),
    Game("pop'n music", ("popn", "9B"), parse_popn),
    Game("GITADORA", ("gitadora", "Dora"), parse_gitadora),
    Game("GITADORA", ("gitadora", "Gita"), parse_gitadora),
    Game("Jubeat", ("jubeat", "Single"), parse_jubeat),
]


def handle_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("games",
                        nargs="+",
                        choices=[f"{g.tachi_gpt[0]}:{g.tachi_gpt[1]}" for g in SUPPORTED_GAMES] + ["all"],
                        help="Choose one or more games to import, or 'all' for all games")
    parser.add_argument("-j", "--json",
                        action="store_true",
                        help="Output JSON file instead of uploading to tachi")
    args = parser.parse_args()
    if "all" in args.games:
        args.games = SUPPORTED_GAMES
    else:
        args.games = [g for g in SUPPORTED_GAMES
                      if f"{g.tachi_gpt[0]}:{g.tachi_gpt[1]}" in args.games]

    return args


if __name__ == "__main__":
    if FLOWER_SESSION == "":
        print("Flower session cookie is not provided. Aborting")
        exit(1)

    args = handle_arguments()

    if not args.json and TACHI_API_KEY == "":
        print("TACHI_API_KEY is not present in config. Please use --json or provide an API KEY")
        exit(1)

    # games with different playtypes come up in same list and dont wanna flood flower with requests
    page_cache = {}
    for game in args.games:
        if game.flower_name not in page_cache:
            url = find_profile_url(game)
            page_data = parse_page(url)
            page_cache[game.flower_name] = page_data

        tachi_json = game.parse(page_cache[game.flower_name])
        if args.json:
            filename = f"score_{game.tachi_gpt[0]}_{game.tachi_gpt[1]}.json"
            with open(filename, "w") as f:
                print("Writing scores to", filename)
                json.dump(tachi_json, f, indent=4)
        else:
            print("Sending score to tachi")
            submit_score(tachi_json)
