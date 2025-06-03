import psycopg2
import csv

conn = psycopg2.connect("dbname='olympics' user='postgres' host='127.0.0.1' password='123'")
cur = conn.cursor()

# staging table
cur.execute("""
    CREATE TABLE IF NOT EXISTS athlete_events (
        id INTEGER,
        name TEXT,
        sex CHAR(1),
        age INTEGER,
        height INTEGER,
        weight INTEGER,
        team TEXT,
        noc CHAR(3),
        games TEXT,
        year INTEGER,
        season TEXT,
        city TEXT,
        sport TEXT,
        event TEXT,
        medal TEXT
    );
""")

# helper
def int_or_none(value):
    return int(value) if value.isdigit() else None

# load CSV
with open('data/athlete_events.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        cur.execute("""
            INSERT INTO athlete_events VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['ID'], row['Name'], row['Sex'], int_or_none(row['Age']), int_or_none(row['Height']), int_or_none(row['Weight']),
            row['Team'], row['NOC'], row['Games'], row['Year'], row['Season'],
            row['City'], row['Sport'], row['Event'], row['Medal']
        ))

conn.commit()
print("CSV loaded into staging table.")

# insert into normalized tables

# NOC
cur.execute("""
    INSERT INTO NOC (noc_code, team_name)
    SELECT DISTINCT noc, team FROM athlete_events
    WHERE noc IS NOT NULL
    ON CONFLICT DO NOTHING;
""")

# Athlete
cur.execute("""
    INSERT INTO Athlete (id, name, sex, noc_code)
    SELECT DISTINCT id, name, sex, noc
    FROM athlete_events
    WHERE id IS NOT NULL
    ON CONFLICT DO NOTHING;
""")

# Sport
cur.execute("""
    INSERT INTO Sport (name)
    SELECT DISTINCT sport
    FROM athlete_events
    WHERE sport IS NOT NULL
    ON CONFLICT DO NOTHING;
""")

# Games
cur.execute("""
    INSERT INTO Games (year, season, city)
    SELECT DISTINCT year, season, city
    FROM athlete_events
    WHERE year IS NOT NULL
    ON CONFLICT DO NOTHING;
""")

# Event
cur.execute("""
    INSERT INTO Event (event, sport_id, games_id)
    SELECT DISTINCT
        s.event,
        sp.id,
        g.id
    FROM athlete_events s
    JOIN Sport sp ON s.sport = sp.name
    JOIN Games g ON s.year = g.year AND s.season = g.season AND s.city = g.city
    ON CONFLICT DO NOTHING;
""")

# Participation
cur.execute("""
    INSERT INTO Participation (athlete_id, event_id, age, height, weight, medal)
    SELECT
        s.id,
        e.id,
        s.age,
        s.height,
        s.weight,
        s.medal
    FROM athlete_events s
    JOIN Event e ON s.event = e.event
    JOIN Sport sp ON s.sport = sp.name AND e.sport_id = sp.id
    JOIN Games g ON s.year = g.year AND s.season = g.season AND s.city = g.city AND e.games_id = g.id;
""")

conn.commit()

cur.execute("DROP TABLE athlete_events;")
conn.commit()

cur.close()
conn.close()
print("Data fully normalized and inserted.")
