FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt-get install -y  libpq-dev gcc
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "ohlc:app", "--host", "0.0.0.0", "--port", "80"]
