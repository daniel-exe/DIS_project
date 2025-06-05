# write all your SQL queries in this file.
from __init__ import conn
from psycopg2 import sql
from flask import request
import re


# QUERY: Top 10 countries by gold medals
def get_top_gold_countries():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT noc, COUNT(*) AS gold_count
            FROM (
                SELECT DISTINCT a.noc, e.id AS event_id, g.year, p.medal
                FROM participation p
                JOIN athlete a ON p.athlete_id = a.id
                JOIN event e ON p.event_id = e.id
                JOIN games g ON e.games_id = g.id
                WHERE p.medal = 'Gold'
            ) AS unique_gold_medals
            GROUP BY noc
            ORDER BY gold_count DESC
            LIMIT 10;
        """)
        return cur.fetchall()

def get_top_athletes():
    with conn.cursor() as cur:
        cur.execute("""
            SELECT a.name, a.noc AS noc_code,
                COUNT(DISTINCT CASE WHEN p.medal = 'Gold' THEN e.id END) AS gold,
                COUNT(DISTINCT CASE WHEN p.medal = 'Silver' THEN e.id END) AS silver,
                COUNT(DISTINCT CASE WHEN p.medal = 'Bronze' THEN e.id END) AS bronze,
                COUNT(DISTINCT CASE WHEN p.medal != 'NA' THEN e.id END) AS total
            FROM athlete a
            JOIN participation p ON a.id = p.athlete_id
            JOIN event e ON p.event_id = e.id
            GROUP BY a.id, a.name, a.noc
            ORDER BY total DESC, gold DESC, silver DESC, bronze DESC
            LIMIT 10;
        """)
        return cur.fetchall()

def get_filter_options():
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT medal FROM participation WHERE medal IS NOT NULL")
        medals = [row[0] if row[0] != 'NA' else 'None' for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT sex FROM athlete")
        sexes = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT name FROM sport ORDER BY name")
        sports = [row[0] for row in cur.fetchall()]

        cur.execute("SELECT DISTINCT year FROM games ORDER BY year")
        years = [row[0] for row in cur.fetchall()]

    return {
        "medals": medals,
        "sexes": sexes,
        "sports": sports,
        "years": years
    }

def get_filtered_participations(sex=None, sport=None, medal=None, year=None):
    query = """
        SELECT DISTINCT a.name, a.sex, s.name AS sport, p.medal, g.year
        FROM participation p
        JOIN athlete a ON p.athlete_id = a.id
        JOIN event e ON p.event_id = e.id
        JOIN sport s ON e.sport_id = s.id
        JOIN games g ON e.games_id = g.id
    """
    filters = []
    params = []

    if sex:
        filters.append("a.sex = %s")
        params.append(sex)

    if sport:
        filters.append("s.name = %s")
        params.append(sport)

    if medal:
        filters.append("p.medal = %s")
        params.append(medal)

    if year:
        filters.append("g.year = %s")
        params.append(year)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += " ORDER BY g.year DESC LIMIT 50;"

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()

def classify_input(query):
    query = query.strip()
    if re.fullmatch(r'\d{4}', query):
        return 'year'
    return 'athlete'

def get_search_results():
    query = request.args.get('query', '')
    page = int(request.args.get('page', 1))
    total_pages = 1
    limit = 50
    offset = (page - 1) * limit
    results = []
    error = None
    if query:
        category = classify_input(query)

        if category == 'year':
            where_condition = 'g.year::text ~ %s'
        else:
            where_condition = 'a.name ~* %s'

        try:
            with conn.cursor() as cur:
                cur.execute(f"""
                    SELECT COUNT(*) FROM(
                        SELECT DISTINCT a.name, a.sex, s.name, p.medal, g.year
                        FROM participation p
                        JOIN athlete a ON p.athlete_id = a.id
                        JOIN event e ON p.event_id = e.id
                        JOIN sport s ON e.sport_id = s.id
                        JOIN games g ON e.games_id = g.id
                        WHERE {where_condition}
                        ) AS subquery
                    """, (query,))
                total_results = cur.fetchone()[0]
                total_pages = max(1, (total_results + limit - 1) // limit)
                cur.execute(f"""
                    SELECT DISTINCT a.name, a.sex, s.name AS sport, p.medal, g.year
                    FROM participation p
                    JOIN athlete a ON p.athlete_id = a.id
                    JOIN event e ON p.event_id = e.id
                    JOIN sport s ON e.sport_id = s.id
                    JOIN games g ON e.games_id = g.id
                    WHERE {where_condition}
                    ORDER BY g.year DESC
                    LIMIT %s OFFSET %s;
                    """, (query, limit, offset))
                results = cur.fetchall()
        except Exception as e:
            error = "The search did not match any participations"
    return (query, results, error, page, total_pages)

def get_sports():
    with conn.cursor() as cur:
        cur.execute("SELECT DISTINCT name FROM sport ORDER BY name")
        return [row[0] for row in cur.fetchall()]

def get_average_athlete_property(prop, sex=None, sport=None, year=None):
    allowed = {"height", "weight", "age"}
    if prop not in allowed:
        return None

    query = f"""
        SELECT ROUND(AVG(p.{prop})::numeric, 2)
        FROM participation p
        JOIN athlete a ON p.athlete_id = a.id
        JOIN event e ON p.event_id = e.id
        JOIN sport s ON e.sport_id = s.id
        JOIN games g ON e.games_id = g.id
    """

    filters = []
    params = []

    if sex:
        filters.append("a.sex = %s")
        params.append(sex)
    if sport:
        filters.append("s.name = %s")
        params.append(sport)
    if year:
        filters.append("g.year = %s")
        params.append(year)

    if filters:
        query += " WHERE " + " AND ".join(filters)

    with conn.cursor() as cur:
        cur.execute(query, params)
        avg = cur.fetchone()[0]
        return avg

def get_medal_counts_by_country_and_year(countries, years=None):
    placeholders = ','.join(['%s'] * len(countries))
    params = [c.upper() for c in countries]

    query = f"""
        SELECT noc, year, COUNT(*) AS medal_count
        FROM (
            SELECT DISTINCT a.noc, g.year, e.id AS event_id, p.medal
            FROM participation p
            JOIN athlete a ON p.athlete_id = a.id
            JOIN event e ON p.event_id = e.id
            JOIN games g ON e.games_id = g.id
            WHERE p.medal IN ('Gold', 'Silver', 'Bronze') AND a.noc IN ({placeholders})
    """

    if years:
        year_placeholders = ','.join(['%s'] * len(years))
        query += f" AND g.year IN ({year_placeholders})"
        params.extend(years)

    query += """
        ) AS unique_medals
        GROUP BY noc, year
        ORDER BY year, noc
    """

    with conn.cursor() as cur:
        cur.execute(query, params)
        return cur.fetchall()
