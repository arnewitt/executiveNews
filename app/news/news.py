
from utils.utils import is_less_than_x_hours_ago

import feedparser
import ssl


class News:
    def __init__(self, hours_limit: int) -> None:
        self.rss_url = None
        self.most_recent_news = []
        self.hours_limit = hours_limit

    def get_news(self):
        raise NotImplementedError()

class TagesschauNews(News):

    def __init__(self, hours_limit: int, news_interest: str = "wirtschaft") -> None:
        super().__init__(hours_limit)
        self.news_interest = news_interest
        self.rss_url = f"https://www.tagesschau.de/{news_interest.lower()}/index~rss2.xml"

    def get_news(self):
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        feed = feedparser.parse(self.rss_url)
        for index, entry in enumerate(feed.entries):
            if not is_less_than_x_hours_ago(entry.published, self.hours_limit):
                continue
            if "Wirtschaft vor acht" in entry.title:
                continue

            body = {
                "index": index,
                "category": self.news_interest,
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "published": entry.published,
                "source": f"Tagesschau {self.news_interest}"
            }
            
            self.most_recent_news.append(body)

class NYTBusinessNews(News):

    def __init__(self, hours_limit: int) -> None:
        super().__init__(hours_limit)
        self.rss_url = "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"

    def get_news(self):
        if hasattr(ssl, '_create_unverified_context'):
            ssl._create_default_https_context = ssl._create_unverified_context

        feed = feedparser.parse(self.rss_url)
        for index, entry in enumerate(feed.entries):
            if not is_less_than_x_hours_ago(entry.published, self.hours_limit):
                continue

            body = {
                "index": index,
                "category": "Business",
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "published": entry.published,
                "source": "New York Times Business News"
            }
            
            self.most_recent_news.append(body)

