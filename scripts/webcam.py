import requests
from datetime import datetime
import os
from pathlib import Path

# Source - https://stackoverflow.com/a/63978199
# Posted by aahnik
# Retrieved 2026-11-13, License - CC BY-SA 4.0
url = "https://weather.windowclean.net/webcam/Latest.jpg"

day = datetime.today().strftime('%Y-%m-%d')
Path("./images/").mkdir(parents=True, exist_ok=True)

with open(f'./images/webcam_{day}.png', 'wb') as f:
    f.write(requests.get(url).content)
