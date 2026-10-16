from typing import List

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from crawler.util import strip_tags, remove_tags, remove_comments, remove_empty_tags

MAX_N_PARAGRAPHS: int = 3
RANDOM_WIKI_ARTICLE_URL = "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite"

# Wikimedia rejects requests without a descriptive User-Agent
HEADERS = {
    "User-Agent": "swiss-geo-crawler/1.0 (https://github.com/chbauman/swiss-geo)"
}

# Retry transient server errors (e.g. HTTP 500 from schweizerfluss.ch)
_retry = Retry(
    total=4,
    backoff_factor=2,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False,
)
SESSION = requests.Session()
SESSION.headers.update(HEADERS)
SESSION.mount("https://", HTTPAdapter(max_retries=_retry))

on_click = "onclick=\"document.getElementById('guess').innerHTML = '{}'\""
t_mid = f'<span id="guess" {on_click} style="background-color:#f88;">{{}}</span>'


def get_and_clean(
    url: str,
    sc_tags: List = None,
    remove_table: bool = True,
    remove_span: bool = True,
    remove_empty: bool = True,
    add_remove_tags: List = None,
):
    if sc_tags is None:
        sc_tags = ["a", "b", "i"]
    response = SESSION.get(url, timeout=60)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary stuff
    strip_tags(soup, sc_tags)
    rem_tag_list = [
        "head",
        "img",
        "sup",
    ]
    if remove_table:
        rem_tag_list += ["table"]
    if remove_span:
        rem_tag_list += ["span"]
    if add_remove_tags is not None:
        rem_tag_list += add_remove_tags
    remove_tags(soup, rem_tag_list)
    remove_comments(soup)
    if remove_empty:
        remove_empty_tags(soup)
    return soup
