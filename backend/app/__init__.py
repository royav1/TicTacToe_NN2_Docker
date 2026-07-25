import sys

from flask import Flask
from flask_cors import CORS

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

app = Flask(__name__)
CORS(app)

from app import routes  # 👈 this imports and registers your routes
