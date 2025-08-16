FROM ghcr.io/blindfoldedsurgery/poetry:3.1.3-pipx-3.12-bookworm

WORKDIR /usr/src/app

ADD poetry.toml .
ADD poetry.lock .
ADD pyproject.toml .
ADD README.md .

ADD src/extmdtohtml/ src/extmdtohtml/

RUN poetry install --no-interaction --ansi --without dev

CMD poetry run python src/extmdtohtml/__main__.py
