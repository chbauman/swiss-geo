import bs4


def strip_tags(soup, invalid_tags):
    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()


def remove_tags(soup, tags):
    for t in tags:
        for tag in soup.findAll(t):
            tag.decompose()


def remove_comments(soup):
    for element in soup(text=lambda text: isinstance(text, bs4.Comment)):
        element.extract()


def remove_empty_tags(soup) -> int:
    ct = 0
    for x in soup.find_all():
        if len(x.get_text(strip=True)) == 0:
            x.extract()
            ct += 1

    return ct
