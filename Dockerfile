FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use OpenAI compatible API endpoint from NVIDIA API catalog
ENV API_KEY=api_key
ENV BASE_URL=base_url

# Define the specific time to run (24-hour format)
ENV TARGET_HOUR=6
ENV TARGET_MINUTE=30

CMD ["python", "app/main.py"]