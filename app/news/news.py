
from datetime import datetime, timedelta
import ssl
import pytz
import feedparser

def is_less_than_x_hours_ago(date_str, hours: int = 24) -> bool:
    """
    Checks if a given date string is less than x amount of hours ago from current system time.
    
    Parameters:
    - date_str (str): The date string to check.
    - hours (int): The number of hours to check against.

    Returns:
    - bool: True if the date is less than x hours ago, False otherwise.
    """
    # Define the date format
    date_format = "%a, %d %b %Y %H:%M:%S %z"
    
    # Parse the date string into a datetime object
    parsed_date = datetime.strptime(date_str, date_format)
    
    # Get the current date and time in UTC
    current_date = datetime.now(pytz.utc)
    
    # Calculate the difference
    time_difference = current_date - parsed_date
    
    # Check if the difference is less than 48 hours
    return time_difference < timedelta(hours=hours)

class News:
    """Base Class for News to be summarized"""

    def __init__(self, hours_limit: int) -> None:
        self.rss_url = None
        self.most_recent_news = []
        self.hours_limit = hours_limit

    def get_news(self):
        raise NotImplementedError()

class TagesschauNews(News):
    """Class to retrieve data from german Tagesschau RSS feed."""

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
    """Class to retrieve data from New York Times Business RSS feed."""

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

