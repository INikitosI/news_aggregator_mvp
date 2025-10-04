import feedparser
from typing import List, Dict

# Список базовых источников (можно вынести в .env или JSON позже)
SOURCES = [
    "https://lenta.ru",
    "https://ria.ru",
    "https://news.mail.ru",
    "https://lenta.ru/rss/",
]

def clean_html(raw_html: str) -> str:
    """Удаляет HTML-теги из текста"""
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(raw_html, "html.parser")
    return soup.get_text()

def fetch_news_from_rss(url: str, limit: int = 5) -> List[Dict]:
    """Получает до `limit` новостей из RSS-ленты"""
    feed = feedparser.parse(url)
    news = []
    for entry in feed.entries[:limit]:
        title = entry.get("title", "").strip()
        content = entry.get("summary", "") or entry.get("description", "")
        content = clean_html(content)
        link = entry.get("link", "")
        source = feed.feed.get("title", url)

        news.append({
            "title": title,
            "content": content,
            "url": link,
            "source": source
        })
    return news
