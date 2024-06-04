
from unittest.mock import MagicMock
from summarizer.summarizer import NewsSummarizer
from news.news import TagesschauNews, NYTBusinessNews

class MockOpenAIClient:
    def chat(self):
        return self

    def completions(self):
        return self

    def create(self, model, messages, temperature, top_p, stream):
        return MagicMock(choices=[MagicMock(message=MagicMock(content="Mock summary"))])

def test_news_summarizer(monkeypatch):
    news_feeds = [TagesschauNews(hours_limit=24), NYTBusinessNews(hours_limit=24)]

    for feed in news_feeds:
        feed.get_news = MagicMock()
        feed.most_recent_news = [
            {
                "index": 0,
                "category": "Business",
                "title": "Sample Title",
                "link": "http://example.com",
                "summary": "Sample Summary",
                "published": "Mon, 01 Jan 2024 12:00:00 +0000",
                "source": "Mock Source"
            }
        ]

    openai_client = MockOpenAIClient()
    summarizer = NewsSummarizer(news_feeds=news_feeds, openai_client=openai_client)

    result = summarizer.summarize_news()
    assert result == "Mock summary"
