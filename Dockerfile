FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV API_KEY=api_key
ENV BASE_URL=base_url

CMD ["python", "app/main.py"]