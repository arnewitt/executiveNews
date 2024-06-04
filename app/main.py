import os
from openai import OpenAI
from news.news import NYTBusinessNews, TagesschauNews
from summarizer.summarizer import NewsSummarizer

def main():
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

if __name__ == "__main__":
    main()