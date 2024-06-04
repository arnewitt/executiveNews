
from typing import List
from openai import OpenAI

from news import News

class NewsSummarizer:
    
    def __init__(self, news_feeds: List[News], openai_client: OpenAI) -> None:
        self.news_feeds = news_feeds
        self._recent_news_summaries = []
        self.client = openai_client

    def _prompt_exec_summary(self, news: str) -> str:
        pre_prompt = "Take the following news and create an executive summary for me. Only take in information from the articles. Don`t create your own content. Your reply should be short and clear, covering the most important things to know about recent events:\n\n"
        post_prompt = "\n\nAlways put the source of information in brackets behind a section (e.g., 'information (publisher)')"
        return pre_prompt + news + post_prompt

    def _prompt_intermediate_summary(self, news: str) -> str:
        pre_prompt = "Take the following news and condense them into a short summary. Only take in information from the articles. Don`t create your own content. Your reply should be short and clear.\n\n"
        post_prompt = "\n\nAlways put the source of information in brackets behind a section (e.g., 'information (publisher)')"
        return pre_prompt + news + post_prompt

    def _fetch_and_summarize_news(self) -> List[str]:
        for news_feed in self.news_feeds:
            news_feed.get_news()
            news_items = ["\n".join([f"{key.capitalize()}: {value}" for key, value in n.items()]) for n in news_feed.most_recent_news]

            if news_items:
                prompt_intermediate_summary = self._prompt_intermediate_summary(news="\n\n".join(news_items))
                summary_news = self._execute_query(prompt_intermediate_summary)
                self._recent_news_summaries.append(summary_news)

        return self._recent_news_summaries

    def _execute_query(self, query: str) -> str:
        response = self.client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=[{"role": "user", "content": query}],
            temperature=0,
            top_p=1,
            stream=False
        )
        return response.choices[0].message.content

    def summarize_news(self) -> str:
        news_summaries = self._fetch_and_summarize_news()
        prompt = self._prompt_exec_summary(news="\n\n".join(news_summaries))
        return self._execute_query(prompt)
