FROM python:3.9-slim-buster

WORKDIR /app

RUN apt-get update && apt-get -y install curl build-essential
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="$PATH:/root/.cargo/bin"

COPY requirements.txt .
RUN pip3 install -r requirements.txt
RUN python3 -m nltk.downloader all

COPY . .

ENTRYPOINT ["/bin/sh", "-c"]
CMD ["uvicorn server:app --host 0.0.0.0 --port 8088"]

