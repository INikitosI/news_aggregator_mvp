import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from parsers.rss_parser import SOURCES, fetch_news_from_rss
from utils.summarizer import nlp_summarize
from typing import List, Dict

app = FastAPI(
    title="Персональный агрегатор новостей (MVP)",
    description="Собирает новости из RSS и генерирует краткую сводку (2–3 предложения)."
)

# Раздача статики (фронтенд)
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.mount("/", StaticFiles(directory="static", html=True), name="root")

def aggregate_all_news() -> List[Dict]:
    all_news = []
    seen_urls = set()
    for url in SOURCES:
        try:
            news_list = fetch_news_from_rss(url, limit=5)
            for item in news_list:
                if item["url"] not in seen_urls:
                    seen_urls.add(item["url"])
                    all_news.append(item)
        except Exception as e:
            print(f"[ERROR] Источник {url} недоступен: {e}")
            continue
    return all_news

@app.get("/api/news", response_model=List[Dict])
def get_news():
    raw_news = aggregate_all_news()
    result = []
    for item in raw_news:
        summary = nlp_summarize(item["content"], sentences_count=2, lang="russian")
        result.append({
            "title": item["title"],
            "summary": summary,
            "url": item["url"],
            "source": item["source"]
        })

    return result

