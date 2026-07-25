import sys
import os

from flask import Flask
from flask_cors import CORS

for stream in (sys.stdout, sys.stderr):
    if hasattr(stream, "reconfigure"):
        stream.reconfigure(encoding="utf-8", errors="replace")

app = Flask(__name__)

allowed_origins = [
    origin.strip()
    for origin in os.getenv("FRONTEND_ORIGINS", "http://localhost:3000").split(",")
    if origin.strip()
]
CORS(app, origins=allowed_origins)

from app import routes  # 👈 this imports and registers your routes
