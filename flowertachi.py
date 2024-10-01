import json
from datetime import datetime

from config import FLOWER_SESSION, FLOWER_PROFILE_URL, TACHI_API_KEY
from dora import parse_dora
from flower import parse_page
from tachi import submit_score

if __name__ == "__main__":
    if FLOWER_PROFILE_URL == "":
        print("Profile URL to import is not provided. Aborting.")
        exit(1)
    if FLOWER_SESSION == "":
        print("Flower session cookie is not provided. Aborting.")
        exit(1)

    songs = parse_page(FLOWER_PROFILE_URL)
    tachi_data = parse_dora(songs)

    cur_time = int(datetime.now().timestamp())
    with open(f"dora-{cur_time}.json", "w") as f:
        f.write(json.dumps(tachi_data, indent=4))

    if TACHI_API_KEY == "":
        print("No tachi API key provided. Not uploading")
    else:
        submit_score(tachi_data)
