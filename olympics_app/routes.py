from flask import render_template
from flask import request
from __init__ import app

@app.route("/")
def home():
    return render_template("layout.html", title="Home")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/top-countries")
def top_countries():
    from models import get_top_gold_countries
    countries = get_top_gold_countries()
    return render_template("top_countries.html", title="Top Countries", countries=countries)

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
    (q, results, error) = get_search_results()
    return render_template('results.html', q=q, results=results, error=error)
