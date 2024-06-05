
import os
import logging
from time import sleep
from datetime import datetime

from news.news import NYTBusinessNews, TagesschauNews, BloombergNews
from summarizer.summarizer import NewsSummarizer 

from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



def run_summarization(
        base_url: str = os.environ.get("BASE_URL", None),
        api_key: str = os.environ.get("API_KEY", None)
):
    """Create a summary of configured RSS feeds."""
    # Setup OpenAI client
    base_url = base_url
    api_key = api_key
    openai_client = OpenAI(base_url=base_url, api_key=api_key)

    # Configure news search
    hours_limit = 6
    news_feeds = [
        TagesschauNews(hours_limit=hours_limit, news_interest="wirtschaft", persist=True),
        NYTBusinessNews(hours_limit, persist=True),
        BloombergNews(hours_limit=hours_limit, persist=True)
    ]

    # Create summary
    news_summarizer = NewsSummarizer(
        news_feeds=news_feeds,
        openai_client=openai_client,
        persist=True
    )
    summary = news_summarizer.summarize_news()

    # Summary can be processed further depending on use case, e.g. sending via e-mail
    print(summary)

def check_time_and_run(target_hour, target_minute):
    """Checks if a report should be created and executes script if required."""
    while True:
        logging.info('Checking the time...')

        # Get the current time
        now = datetime.now()
        current_hour = now.hour
        current_minute = now.minute

        # Check if the current time matches the target time
        if current_hour == target_hour and current_minute == target_minute:
            logging.info('Target time reached, running summarization...')
            run_summarization()
            logging.info('Summarization completed.')
            # Wait for 60 seconds to avoid running multiple times within the same minute
            sleep(60)
        else:
            # Sleep for a short time to avoid busy waiting
            sleep(30)