import re

import httpx
import mistune
from flask import Flask, Response

BASE_URL = "https://sos-de-fra-1.exo.io/md2html"

app = Flask(__name__)


def get_url(path: str) -> str:
    url = "/".join([BASE_URL, path])
    response = httpx.get(url, timeout=15, follow_redirects=True)
    response.raise_for_status()

    return response.text.strip()


def md_to_html(md: str) -> str:
    return mistune.html(md)


@app.get("/<path:path>")
@app.get("/", defaults={"path": None})
def index(path: str | None):
    try:
        md = md_to_html(get_url(path))
    except httpx.HTTPStatusError:
        return Response(
            f"Markdown document not found on remote <code>{BASE_URL}/{path}</code>",
            404
        )
    body = md_to_html(md)
    title = "md2html"
    if match := re.search(r"<h1>(.*?)</h1>", body, re.IGNORECASE | re.UNICODE):
        title = match.group(1)

    return f"""<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
  </head>
  <body>
    {body}
  </body>
</html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)