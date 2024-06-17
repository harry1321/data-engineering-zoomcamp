FROM python:3.11-slim

RUN apt-get update && apt-get install -y curl

COPY ./postgres_python/requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash" ]
