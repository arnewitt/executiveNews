import pytz
from datetime import datetime, timedelta
from app.news.news import TagesschauNews, NYTBusinessNews

class MockFeedEntry:
    def __init__(self, title, link, summary, published):
        self.title = title
        self.link = link
        self.summary = summary
        self.published = published

class MockFeed:
    def __init__(self, entries):
        self.entries = entries

def mock_parse(url):
    recent_time = (datetime.now(pytz.utc) - timedelta(hours=1)).strftime("%a, %d %b %Y %H:%M:%S %z")
    if "tagesschau" in url:
        return MockFeed([
            MockFeedEntry("Title 1", "http://example.com/1", "Summary 1", recent_time),
            MockFeedEntry("Wirtschaft vor acht", "http://example.com/2", "Summary 2", recent_time)
        ])
    elif "nyt" in url:
        return MockFeed([
            MockFeedEntry("Title 3", "http://example.com/3", "Summary 3", recent_time)
        ])

def test_tagesschau_news(monkeypatch):
    monkeypatch.setattr("feedparser.parse", mock_parse)
    news = TagesschauNews(hours_limit=24)
    news.get_news()
    assert len(news.most_recent_news) == 1
    assert news.most_recent_news[0]["title"] == "Title 1"

def test_nyt_business_news(monkeypatch):
    monkeypatch.setattr("feedparser.parse", mock_parse)
    news = NYTBusinessNews(hours_limit=24)
    news.get_news()
    assert len(news.most_recent_news) == 1
    assert news.most_recent_news[0]["title"] == "Title 3"
