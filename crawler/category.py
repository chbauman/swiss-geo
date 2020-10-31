from typing import List

from crawler import get_and_clean

BASE_URL = "https://de.wikipedia.org/wiki/Kategorie:{}"
WIKI_URL = "https://de.wikipedia.org{}"

categories = [
    "Mathematik", "Physics",
]


def scrape_category(current_url_lists: List[str], url: str):
    """Scrapes a category recursively."""
    soup = get_and_clean(url, sc_tags=["b", "i"])
    sub_categories = soup.findAll("div", {"class": "mw-category-group"})

    for s in sub_categories:
        for li in s.findAll("li"):
            a_tag = li.find("a")
            h_attr = a_tag.attrs["href"]
            if "Kategorie" in h_attr:
                scrape_category(current_url_lists, WIKI_URL.format(h_attr))
            elif "List" in h_attr:
                continue
            else:
                current_url_lists.append(h_attr)

    pass


def scrape_swiss_villages():
    url = "https://de.wikipedia.org/wiki/Liste_Schweizer_Gemeinden"
    soup = get_and_clean(url, remove_table=False)
    village_table = soup.find("table", {"class": "wikitable"})
    res_list = []
    for v in village_table.findAll("tr"):
        entry = [dat.text.strip() for dat in v.findAll("td")]
        if len(entry) == 6:
            res_list.append(entry)
            print(entry)
    return res_list
