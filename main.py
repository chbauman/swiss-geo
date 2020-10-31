import json
import os
from pathlib import Path

from crawler.category import scrape_swiss_villages

PROJECT_DIR = Path(__file__).parent

if __name__ == "__main__":
    rl = scrape_swiss_villages()

    write_path = os.path.join(PROJECT_DIR, "data", "gem.json")
    with open(write_path, "w") as f:
        json.dump(rl, f)
