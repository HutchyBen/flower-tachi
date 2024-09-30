from datetime import datetime
import requests
from bs4 import BeautifulSoup
import json

from dora import parse_dora

s = requests.Session()
s.cookies.set("flower_session", "MODIFY")
res = s.get("https://projectflower.eu/game/gitadora/profile/MODIFY")
soup = BeautifulSoup(res.text, "html.parser")

data = parse_dora(soup)
cur_time = int(datetime.now().timestamp())
with open(f"dora-{cur_time}.json", "w") as f:
    f.write(json.dumps(data, indent=4))
