FROM docker.io/python:3.10

WORKDIR /

# --- [Install python and pip] ---
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y python3 python3-pip git
COPY . /

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# --- ADDED TIMEOUT FOR FIX ---
ENV GUNICORN_CMD_ARGS="--workers=3 --bind=0.0.0.0:8080 --timeout=1000"

EXPOSE 8080

CMD [ "gunicorn", "main:app" ]