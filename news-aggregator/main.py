from fastapi import FastAPI

app = FastAPI(title="News Aggregator MVP")

@app.get("/")
def root():
    return {"message": "Welcome to News Aggregator API"}

@app.get("/api/news")
def get_news():
    # временно — заглушка
    return [{"title": "Test", "summary": "Test summary", "url": "https://example.com", "source": "Test"}]
