FROM python:3.10-slim

WORKDIR /code

COPY requirements.txt requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r requirements.txt

COPY . .

CMD ["uvicorn", "recriver:app", "--host "0.0.0.0", "--port", "80"]
