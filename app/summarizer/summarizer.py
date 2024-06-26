
from typing import List
from openai import OpenAI
from datetime import datetime
from news.news import News
import json
import os

class NewsSummarizer:
    """Used to summarize news from RSS feeds."""
    
    def __init__(self, news_feeds: List[News], openai_client: OpenAI, persist: bool = False) -> None:
        self.news_feeds = news_feeds
        self._recent_news_summaries = []
        self.client = openai_client
        self.persist = persist

    def _prompt_exec_summary(self, news: str) -> str:
        """
        Wraps a news element with a pre-prompt and a post-prompt to create the final exec summary.

        Parameters:
        - news (str): The news element to wrap.

        Returns:
        - str: The wrapped news element.
        """
        pre_prompt = "Take the following news and create an executive summary for me. Only take in information from the articles. Don`t create your own content. Your reply should be short and clear, covering the most important things to know about recent events:\n\n"
        post_prompt = "\n\nAlways put the source of information in brackets behind a section (e.g., 'information (publisher)')"
        return pre_prompt + news + post_prompt

    def _prompt_intermediate_summary(self, news: str) -> str:
        """
        Wraps a news element with a pre-prompt and a post-prompt to create a summary of all news articles from one source.

        Parameters:
        - news (str): The news element to wrap.

        Returns:
        - str: The wrapped news element.
        """
        pre_prompt = "Take the following news and condense them into a short summary. Only take in information from the articles. Don`t create your own content. Your reply should be short and clear.\n\n"
        post_prompt = "\n\nAlways put the source of information in brackets behind a section (e.g., 'information (publisher)')"
        return pre_prompt + news + post_prompt

    def _fetch_and_summarize_news(self) -> List[str]:
        """Iterate over all news feeds and create summaries for each."""
        for news_feed in self.news_feeds:
            news_feed.get_news()
            news_items = ["\n".join([f"{key.capitalize()}: {value}" for key, value in n.items()]) for n in news_feed.most_recent_news]

            if news_items:
                prompt_intermediate_summary = self._prompt_intermediate_summary(news="\n\n".join(news_items))
                summary_news = self._execute_query(prompt_intermediate_summary)
                
                if self.persist == True:
                    self.persist_summary(summary_news, filename=f"intermediate-{datetime.now()}.md")
                
                self._recent_news_summaries.append(summary_news)

        return self._recent_news_summaries
    
    def summarize_news(self) -> str:
        """
        Creates the final summary of all news articles from all sources.

        Returns:
        - str: The final response with exec summary.
        """
        news_summaries = self._fetch_and_summarize_news()
        prompt = self._prompt_exec_summary(news="\n\n".join(news_summaries))
        exec_summary = self._execute_query(prompt)

        if self.persist == True:
            self.persist_summary(exec_summary, filename=f"executive-{datetime.now()}.md")
        
        return exec_summary

    def _execute_query(self, query: str) -> str:
        """
        Request a response from a LLM to a given query.

        Parameters:
        - query (str): The query to be answered.

        Returns:
        - str: The response from the LLM.
        """
        response = self.client.chat.completions.create(
            model="meta/llama3-70b-instruct",
            messages=[{"role": "user", "content": query}],
            temperature=0,
            top_p=1,
            stream=False
        )
        return response.choices[0].message.content

    def persist_summary(self, summary: str, filename: str):
        """
        Store data with summary in a Markdown file. Can be empty.

        Parameters:
        - summary (str): The summary to store.
        - filename (str): The filename to store the summary in.
        """
        directory = "./app/data/summary/"
        file_path = f"{directory}{filename}"
        
        if self.persist == True:
            if not os.path.exists(directory):
                os.makedirs(directory)

            with open(file_path, "w") as file:
                json.dump(summary, file)