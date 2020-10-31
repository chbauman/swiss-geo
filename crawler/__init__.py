from typing import List

import requests
from bs4 import BeautifulSoup

from crawler.util import strip_tags, remove_tags, remove_comments, remove_empty_tags

MAX_N_PARAGRAPHS: int = 3
RANDOM_WIKI_ARTICLE_URL = "https://de.wikipedia.org/wiki/Spezial:Zuf%C3%A4llige_Seite"

on_click = "onclick=\"document.getElementById('guess').innerHTML = '{}'\""
t_mid = f'<span id="guess" {on_click} style="background-color:#f88;">{{}}</span>'


def get_and_clean(url: str, sc_tags: List = None, remove_table: bool = True,
                  remove_span: bool = True, remove_empty: bool = True, add_remove_tags: List = None):
    if sc_tags is None:
        sc_tags = ["a", "b", "i"]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unnecessary stuff
    strip_tags(soup, sc_tags)
    rem_tag_list = ["head", "img", "sup",]
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
