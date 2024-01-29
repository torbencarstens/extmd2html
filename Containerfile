FROM ghcr.io/blindfoldedsurgery/poetry:1.1.1-pipx-3.12-bookworm

RUN apt-get update && \
    apt-get install gcc -y && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

ADD poetry.toml .
ADD poetry.lock .
ADD pyproject.toml .

RUN poetry install --no-interaction --ansi --only-root

ADD src/extmdtohtml/ .

CMD poetry run python src/extmdtohtml/__main__.py
