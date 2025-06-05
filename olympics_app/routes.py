from flask import Flask, render_template, request, redirect, url_for, jsonify
from __init__ import app, conn

@app.route("/")
def home():
    return render_template("home.html", title="Home")

@app.route("/leaderboards")
def leaderboards():
    from models import get_top_gold_countries
    countries = get_top_gold_countries()
    return render_template("leaderboards.html", title="Leaderboards", countries=countries)

@app.route("/participations", methods=["GET", "POST"])
def participations():
    from models import get_filtered_participations, get_filter_options

    filters = get_filter_options()
    results = []

    if request.method == "POST":
        medal = request.form.get("medal")
        sex = request.form.get("sex")
        sport = request.form.get("sport")
        year = request.form.get("year")

        medal = None if medal == "Any" or medal == "None" else medal
        sex = None if sex == "Any" else sex
        sport = None if sport == "Any" else sport
        year = int(year) if year and year != "Any" else None

        results = get_filtered_participations(
            sex=sex,
            sport=sport,
            medal=medal,
            year=year
        )

    return render_template("participations.html", title="Athelete Participations", filters=filters, results=results)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/search/results', methods=['GET'])
def search_results():
    from models import classify_input, get_search_results
    (query, results, error, page, total_pages) = get_search_results()
    return render_template('results.html', query=query, results=results, error=error, page=page, total_pages=total_pages)

@app.route("/interactive-stats", methods=["GET", "POST"])
def interactive_stats():
    from models import get_filter_options, get_sports, get_average_athlete_property

    filters = get_filter_options()
    sports = get_sports()
    results = None

    if request.method == "POST":
        prop = request.form.get("property")
        sex = request.form.get("sex")
        sport = request.form.get("sport")
        year = request.form.get("year")

        sex = None if sex == "Any" else sex
        sport = None if sport == "Any" else sport
        year = int(year) if year and year != "Any" else None

        results = get_average_athlete_property(prop, sex, sport, year)

    return render_template("interactive_stats.html", title="Average Athlete Stats", filters=filters, sports=sports, results=results)

@app.route("/medal-chart-data", methods=["POST"])
def medal_chart_data():
    from models import get_medal_counts_by_country_and_year

    countries = request.json.get("countries", [])
    years = request.json.get("years", [])

    if not countries:
        return jsonify({"error": "No countries selected"}), 400

    results = get_medal_counts_by_country_and_year(countries, years)

    counts = {country: {year: 0 for year in years} for country in countries}

    for country, year, count in results:
        counts[country][year] = count

    response = {
        "years": years,
        "data": [
            {
                "country": country,
                "counts": [counts[country].get(year, 0) for year in years]
            }
            for country in countries
        ]
    }

    return jsonify(response)
