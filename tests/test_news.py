
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
    if "tagesschau" in url:
        return MockFeed([
            MockFeedEntry("Title 1", "http://example.com/1", "Summary 1", "Mon, 01 Jan 2024 12:00:00 +0000"),
            MockFeedEntry("Wirtschaft vor acht", "http://example.com/2", "Summary 2", "Mon, 01 Jan 2024 12:00:00 +0000")
        ])
    elif "nyt" in url:
        return MockFeed([
            MockFeedEntry("Title 3", "http://example.com/3", "Summary 3", "Mon, 01 Jan 2024 12:00:00 +0000")
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
