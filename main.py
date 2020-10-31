from pathlib import Path

from crawler.category import scrape_swiss_villages, scrape_swiss_mountains

PROJECT_DIR = Path(__file__).parent

if __name__ == "__main__":
    scrape_swiss_mountains(PROJECT_DIR)
    scrape_swiss_villages(PROJECT_DIR)
    pass
