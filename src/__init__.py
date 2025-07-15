from flask import Flask

app = Flask(__name__)
tasks = []

from src import routes