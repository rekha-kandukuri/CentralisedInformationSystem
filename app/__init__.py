from flask import Flask, redirect, render_template, url_for
from config import config

app = Flask(__name__)
app.config.from_object(config)

@app.route('/')
def home():
    return "Home"