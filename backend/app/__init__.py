from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from app import routes  # 👈 this imports and registers your routes
