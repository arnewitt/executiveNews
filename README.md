# executiveNews
This project provides a streamlined way to fetch and summarize the latest news from various sources. It leverages RSS feeds and integrates with the OpenAI API to generate concise summaries of recent news articles. The aim is to deliver clear, important information without the noise, making it easier to stay informed.

# News Summarizer

This project provides a streamlined way to fetch and summarize the latest news from various sources. It leverages RSS feeds and integrates with the OpenAI API to generate concise summaries of recent news articles. The aim is to deliver clear, important information without the noise, making it easier to stay informed.

## Features

- Fetches news articles from multiple RSS feeds.
- Summarizes content using OpenAI's language model.
- Configurable to include specific news categories.
- Filters articles by publication time (last 24 hours is default).

## Requirements

- Python 3.10+
- Docker (optional, for containerized setup)
- API key for LLM that is OpenAI compatible (e.g. OpenAI, NVIDIA API Catalogue, etc.)

## Run

1. Clone project with `git clone https://github.com/arnewitt/executiveNews.git && cd executiveNews`
2. With Docker:
  - Update Dockerfile with your credentials
  - Build container with `docker build -t executivenews . && docker run -e API_KEY=your_api_key -e BASE_URL=your_base_url executivenews`
3. Without Docker:
  - Set environment variables with `export API_KEY="your_api_key" export BASE_URL="your_base_url"` 
  - Execute main script with `pip install -r requirements.txt && python app/main.py`
4. ??
5. Profit

## Contributing

Contributions are welcome! Please open issues or submit pull requests for any improvements or new features.