import json
import os

from crawler import get_and_clean


def scrape_swiss_villages(project_dir: str) -> None:
    url = "https://de.wikipedia.org/wiki/Liste_Schweizer_Gemeinden"
    soup = get_and_clean(url, remove_table=False)
    village_table = soup.find("table", {"class": "wikitable"})
    res_list = []
    for v in village_table.findAll("tr"):
        entry = [dat.text.strip() for dat in v.findAll("td")]
        if len(entry) == 6:
            if f"({entry[1]})" in entry[0]:
                entry[0] = entry[0][:-5]
            res_list.append(entry)
            print(entry)

    # Save to json
    write_path = os.path.join(project_dir, "data", "gem.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)


def scrape_swiss_mountains(project_dir: str) -> None:
    url = "https://de.wikipedia.org/wiki/Liste_von_Bergen_in_der_Schweiz"
    soup = get_and_clean(url, remove_table=False)
    village_table = soup.findAll("table", {"class": "wikitable"})[1]
    res_list = []
    for v in village_table.findAll("tr"):
        entry = [dat.text.strip() for dat in v.findAll("td")]
        if len(entry) >= 6:
            entry = entry[:2] + [e.split(" ")[0] for e in entry[-2:]]
            res_list.append(entry)
            print(entry)

    # Save to json
    print(f"Total {len(res_list)} Swiss mountains.")
    write_path = os.path.join(project_dir, "data", "mount.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)
    return
