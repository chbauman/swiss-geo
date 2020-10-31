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
            # print(entry)

    # Save to json
    print(f"Total {len(res_list)} Swiss gemeinden.")
    write_path = os.path.join(project_dir, "data", "gem.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)


def scrape_swiss_mountains(project_dir: str) -> None:
    url = "https://de.wikipedia.org/wiki/Liste_von_Bergen_in_der_Schweiz"
    soup = get_and_clean(url, remove_table=False)
    mount_table = soup.findAll("table", {"class": "wikitable"})[1]
    res_list = []
    for v in mount_table.findAll("tr"):
        entry = [dat.text.strip() for dat in v.findAll("td")]
        if len(entry) >= 6:
            entry = entry[:2] + [e.split(" ")[0] for e in entry[-2:]]
            res_list.append(entry)
            # print(entry)

    # Save to json
    print(f"Total {len(res_list)} Swiss mountains.")
    write_path = os.path.join(project_dir, "data", "mount.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)
    return


def scrape_swiss_lakes(project_dir: str) -> None:
    url = "https://de.wikipedia.org/wiki/Liste_der_Seen_in_der_Schweiz"
    soup = get_and_clean(url, remove_table=False)
    soup_el = soup.find("div", {"class": "mw-content-ltr"})
    soup_el = soup_el.findAll("ul",)[1]
    res_list = []
    for v in soup_el.findAll("li"):
        url_part = "_".join(v.text.split(" "))
        c = " ".join(v.text.split(" ")[-2:])
        if c.startswith("im"):
            c = "Kanton " + c[3:]
        new_url = f"https://de.wikipedia.org/wiki/{url_part}"
        sub_soup = get_and_clean(new_url, remove_table=False, remove_span=False, remove_empty=False)
        lake_table = sub_soup.find("table", {"class": "wikitable"})
        for v_inner in lake_table.findAll("tr"):
            entry = [dat.text.strip() for dat in v_inner.findAll("td")]
            if len(entry) > 0:
                entry = [c] + entry[1:3] + entry[5:7]
                res_list.append(entry)
                # print(entry)

    # Save to json
    print(f"Total {len(res_list)} Swiss lakes.")
    write_path = os.path.join(project_dir, "data", "lakes.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)
    return


def scrape_swiss_passes(project_dir: str) -> None:
    url = "https://de.wikipedia.org/wiki/Liste_der_Pässe_in_der_Schweiz"
    soup = get_and_clean(url, remove_table=False, remove_empty=False, remove_span=False, sc_tags=["b", "i"])
    mount_table = soup.findAll("table", {"class": "wikitable"})[0]
    res_list = []
    for v in mount_table.findAll("tr"):
        all_td = list(v.findAll("td"))
        if len(all_td) > 6:
            src_kt = all_td[1].find("span").text
            src_gem = all_td[1].findAll("a")[1].text
            dst_kt = all_td[2].find("span").text
            dst_gem = all_td[2].findAll("a")[1].text
            entry = [dat.text.strip() for dat in all_td][:5]
            entry = [entry[0], src_kt, src_gem, dst_kt, dst_gem, str(int(entry[-2])), str(int(entry[-1]))]
            res_list.append(entry)
            # print(entry)

    # Save to json
    print(f"Total {len(res_list)} Swiss passes.")
    write_path = os.path.join(project_dir, "data", "pass.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)
    return


c_list = [
    "Zürich",
    "Bern",
    "Luzern",
    "Uri",
    "Schwyz",
    "Obwalden",
    "Nidwalden",
    "Glarus",
    "Zug",
    "Freiburg",
    "Solothurn",
    "Basel-Stadt",
    "Basel-Landschaft",
    "Schaffhausen",
    "Appenzell-ausserrhoden",
    "Appenzell-innerrhoden",
    "st-Gallen",
    "Graubünden",
    "Aargau",
    "Thurgau",
    "Tessin",
    "Waadt",
    "Wallis",
    "Neuenburg",
    "Genf",
    "Jura",
]


def scrape_swiss_rivers(project_dir: str) -> None:
    url = "https://schweizerfluss.ch/"
    res_list = []

    for k in c_list:
        k_new = k.lower().replace("ü", "ue").replace("ö", "oe").replace("ä", "ae")

        ct = 1
        max_pages = 10000
        while True:
            k_url = url + "kanton/" + k_new
            if ct > 1:
                k_url = f"{k_url}/page/{ct}/"
            soup = get_and_clean(k_url, remove_table=False, remove_empty=False, remove_span=False,
                                 sc_tags=["b", "i"], add_remove_tags=["script"])
            res_boxes = soup.findAll("div", {"class": "resultbox"})
            for r in res_boxes:
                name = r.find("h2").text.replace(u'\xa0', u' ').strip()
                cantons = r.find("h3").text.replace(u'\xa0', u' ').strip()
                length = r.find("span").text.replace(u'\xa0', u' ').strip()
                len_int = int(length.split(" ")[1])
                if len_int < 10:
                    continue
                river_class = r.findAll("span")[-1].text.replace(u'\xa0', u' ').strip()
                river_class = " ".join(river_class.split(" ")[:-1])
                entry = [name, cantons, length[7:], river_class[8:]]
                res_list.append(entry)
                print(entry)

            # Find number of sub pages
            if ct == 1:
                pn = soup.findAll("a", {"class": "page-numbers"})
                if len(pn) == 0:
                    break
                pn = pn[-2]
                max_pages = int(pn.text)
                pass
            ct += 1
            if ct > max_pages:
                break

    # Save to json
    print(f"Total {len(res_list)} Swiss rivers.")
    write_path = os.path.join(project_dir, "data", "river.json")
    with open(write_path, "w") as f:
        json.dump(res_list, f)
    return
