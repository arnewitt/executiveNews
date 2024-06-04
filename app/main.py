import os
from time import sleep
from datetime import datetime
from openai import OpenAI
from news.news import NYTBusinessNews, TagesschauNews
from summarizer.summarizer import NewsSummarizer


def run_summarization():
    # Setup OpenAI client
    base_url = os.environ.get("BASE_URL", None)
    api_key = os.environ.get("API_KEY", None)

    openai_client = OpenAI(
        base_url=base_url,
        api_key=api_key
    )

    # Configure news search
    hours_limit = 24
    news_feeds = [
        TagesschauNews(hours_limit=hours_limit, news_interest="wirtschaft"),
        NYTBusinessNews(hours_limit)
    ]

    # Create summary
    news_summarizer = NewsSummarizer(news_feeds=news_feeds, openai_client=openai_client)
    summary = news_summarizer.summarize_news()

    print(summary)

def check_time_and_run(target_hour, target_minute):
    while True:
        # Get the current time
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Check if the current time matches the target time
        if current_hour == target_hour and current_minute == target_minute:
            run_summarization()
            # Wait for 60 seconds to avoid running multiple times within the same minute
            sleep(60)
        else:
            # Sleep for a short time to avoid busy waiting
            sleep(30)

if __name__ == "__main__":
    # Define the specific time to run (24-hour format)
    target_hour = 7
    target_minute = 30

    check_time_and_run(target_hour, target_minute)