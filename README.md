# News Summarizer

This project provides a streamlined way to fetch and summarize the latest news from various sources. It leverages RSS feeds and integrates with an OpenAI compatible API to generate short summaries of recent news articles. The aim is to deliver clear, important information without the noise, making it easier to stay informed. Currently it uses Llama3-70b from the [NVIDIA API catalog](https://build.nvidia.com/meta/llama3-70b).  

## Features

- Fetches news articles from multiple RSS feeds.
  - It summarizes recent articles for each source, and then creates a final summary.
  - Based on experience, it currently works better with fewer sources (3 or less)
- Summarizes content using OpenAI's language model.
- Configurable to include specific news categories.
- Filters articles by publication time (last 24 hours is default).

## Requirements

- Python 3.10+
- Docker (optional, for containerized setup)
- Valid API key and URL

## Run

1. Clone project with `git clone https://github.com/arnewitt/executiveNews.git && cd executiveNews`
2. Test with pytest by using `PYTHONPATH=./app python -m pytest tests/`
3. With Docker:
  - Update Dockerfile with your credentials
  - Build and run container with `docker build -t executivenews . && docker run -e API_KEY=your_api_key -e BASE_URL=your_base_url executivenews`
4. Without Docker:
  - Set environment variables with `export API_KEY="your_api_key" export BASE_URL="your_base_url"` 
  - Install dependencies and execute main script with `pip install -r requirements.txt && python app/main.py`
5. ??
6. Profit

## Contributing

Contributions are welcome! Please open issues or submit pull requests for any improvements or new features.