FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt requirements.txt

# curl sert aux healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip \
  && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80

CMD ["python", "app.py"]

