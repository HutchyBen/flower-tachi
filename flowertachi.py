import json
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from config import FLOWER_SESSION, FLOWER_PROFILE_URL, TACHI_API_KEY
from dora import parse_dora
from tachi import submit_score

if __name__ == "__main__":
    if FLOWER_PROFILE_URL == "":
        print("Profile URL to import is not provided. Aborting.")
        exit(1)
    if FLOWER_SESSION == "":
        print("Flower session cookie is not provided. Aborting.")
        exit(1)

    s = requests.Session()
    s.cookies.set("flower_session", FLOWER_SESSION)
    res = s.get(FLOWER_PROFILE_URL)
    soup = BeautifulSoup(res.text, "html.parser")

    data = parse_dora(soup)
    cur_time = int(datetime.now().timestamp())
    with open(f"dora-{cur_time}.json", "w") as f:
        f.write(json.dumps(data, indent=4))

    if TACHI_API_KEY == "":
        print("No tachi API key provided. Not uploading")
    else:
        submit_score(data)
