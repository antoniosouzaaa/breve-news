import socket
import feedparser
from typing import Dict, List

socket.setdefaulttimeout(10)

FEEDS = {
    "cultura": [
        {"name": "G1 Pop & Arte", "url": "https://g1.globo.com/rss/g1/pop-arte/"},
        {"name": "Folha Ilustrada", "url": "https://feeds.folha.uol.com.br/ilustrada/rss091.xml"},
        {"name": "CartaCapital Cultura", "url": "https://www.cartacapital.com.br/cultura/feed/"}
    ],
    "economia": [
        {"name": "InfoMoney", "url": "https://www.infomoney.com.br/feed/"},
        {"name": "G1 Economia", "url": "https://g1.globo.com/rss/g1/economia/"}
    ],
    "f1": [
        {"name": "Motorsport Brasil", "url": "https://motorsport.uol.com.br/rss/f1/news/"},
        {"name": "GE Motor", "url": "https://ge.globo.com/rss/ge/motor/"},
        {"name": "F1Mania", "url": "https://www.f1mania.net/feed/"}
    ],
    "design": [
        {"name": "Casa Vogue", "url": "https://casavogue.globo.com/rss/casavogue/"},
        {"name": "Designerd", "url": "https://www.designerd.com.br/feed/"},
        {"name": "ArchDaily Brasil", "url": "https://www.archdaily.com.br/br/feed"}
    ],
    "geral": [
        {"name": "BBC News Brasil", "url": "https://feeds.bbci.co.uk/portuguese/rss.xml"},
        {"name": "Agência Brasil", "url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml"},
        {"name": "G1 Brasil", "url": "https://g1.globo.com/rss/g1/brasil/"}
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
