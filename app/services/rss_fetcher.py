import feedparser
from typing import Dict, List

FEEDS = {
    "cultura": [
        {"name": "The Summer Hunter", "url": "https://thesummerhunter.com/feed/"},
        {"name": "Nexo Cultura", "url": "https://www.nexojornal.com.br/rss/cultura.xml"}
    ],
    "economia": [
        {"name": "Valor Econômico", "url": "https://valor.globo.com/rss/brasil/"},
        {"name": "InfoMoney", "url": "https://www.infomoney.com.br/feed/"}
    ],
    "f1": [
        {"name": "Motorsport F1", "url": "https://motorsport.uol.com.br/rss/f1/news/"},
        {"name": "Grande Prêmio", "url": "https://www.grandepremio.com.br/feed/"}
    ],
    "design": [
        {"name": "Dezeen", "url": "https://www.dezeen.com/feed/"},
        {"name": "Designboom", "url": "https://www.designboom.com/feed/"}
    ],
    "geral": [
        {"name": "BBC News Brasil", "url": "https://feeds.bbci.co.uk/portuguese/rss.xml"},
        {"name": "Agência Brasil", "url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml"}
    ]
}

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

def fetch_category_items(category: str, limit_raw: int = 6) -> List[Dict]:
    items = []
    feed_sources = FEEDS.get(category, [])
    for source in feed_sources:
        try:
            parsed = feedparser.parse(source["url"], agent=USER_AGENT)
            for entry in parsed.entries[:limit_raw]:
                title = entry.get("title", "").strip()
                summary = (entry.get("summary", "") or entry.get("description", "")).strip()
                link = entry.get("link", "").strip()
                if title:
                    items.append({
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "source": source["name"]
                    })
        except Exception as e:
            print(f"Erro ao ler RSS {source['name']}: {e}")
            continue
    return items
