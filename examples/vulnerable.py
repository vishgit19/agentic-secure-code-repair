import requests
from flask import Flask

app = Flask(__name__)


def fetch(url: str) -> None:
    requests.get(url, verify=False, timeout=10)


if __name__ == "__main__":
    app.run(debug=True)
