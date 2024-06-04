import pytest
from unittest.mock import MagicMock, patch
from app.summarizer.summarizer import NewsSummarizer
from app.news.news import TagesschauNews, NYTBusinessNews

class MockOpenAIClient:
    def __init__(self):
        self.chat_mock = MagicMock()

    @property
    def chat(self):
        return self.chat_mock

def mock_completions_create(model, messages, temperature, top_p, stream):
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
    openai_client.chat.completions.create = MagicMock(return_value=MagicMock(choices=[MagicMock(message=MagicMock(content="Mock summary"))]))

    summarizer = NewsSummarizer(news_feeds=news_feeds, openai_client=openai_client)

    with patch.object(summarizer, '_execute_query', return_value="Mock summary") as mock_execute_query:
        result = summarizer.summarize_news()
        assert result == "Mock summary"
        mock_execute_query.assert_called()
