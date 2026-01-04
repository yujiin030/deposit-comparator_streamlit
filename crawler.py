import requests
from bs4 import BeautifulSoup
import pandas as pd

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def crawl_news(keyword="경제", max_page=3):
    titles = []
    links = []

    for page in range(1, max_page + 1):
        url = f"https://search.daum.net/search?w=news&q={keyword}&p={page}"
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "v.daum.net" in href:
                title = a.get_text(strip=True)
                if title:
                    titles.append(title)
                    links.append(href)

    df = pd.DataFrame({
        "title": titles,
        "link": links
    }).drop_duplicates()

    return df
