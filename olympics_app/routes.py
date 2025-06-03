from flask import render_template
from __init__ import app

@app.route("/")
def home():
    return render_template("layout.html", title="Home")

@app.route("/top-countries")
def top_countries():
    from models import get_top_gold_countries
    countries = get_top_gold_countries()
    return render_template("top_countries.html", title="Top Countries", countries=countries)