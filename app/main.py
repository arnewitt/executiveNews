import os
from openai import OpenAI
from news.news import NYTBusinessNews, TagesschauNews
from summarizer.summarizer import NewsSummarizer
from utils.utils import check_time_and_run


def run_summarization():
    # Setup OpenAI client
    base_url = os.environ.get("BASE_URL", None)
    api_key = os.environ.get("API_KEY", None)
    openai_client = OpenAI(base_url=base_url, api_key=api_key)

    # Configure news search
    hours_limit = 24
    news_feeds = [
        TagesschauNews(hours_limit=hours_limit, news_interest="wirtschaft"),
        NYTBusinessNews(hours_limit)
    ]

    # Create summary
    news_summarizer = NewsSummarizer(news_feeds=news_feeds, openai_client=openai_client)
    summary = news_summarizer.summarize_news()

    # Summary can be processed further depending on use case, e.g. sending via e-mail
    print(summary)


if __name__ == "__main__":
    # Define the specific time to run (24-hour format)
    target_hour = 7
    target_minute = 30

    check_time_and_run(target_hour, target_minute)