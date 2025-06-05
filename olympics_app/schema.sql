\i schema_drop.sql

CREATE TABLE IF NOT EXISTS NOC(
	noc varchar(3) PRIMARY KEY,
    team_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Athlete(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    sex CHAR(1) CHECK (sex IN ('M', 'F')),
    noc CHAR(3) REFERENCES NOC(noc)
);

CREATE TABLE IF NOT EXISTS Sport(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Games(
    id SERIAL PRIMARY KEY,
    year INTEGER NOT NULL,
    season TEXT CHECK (season IN ('Summer', 'Winter')),
    city TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Event(
    id SERIAL PRIMARY KEY,
    event TEXT NOT NULL,
    sport_id INTEGER REFERENCES Sport(id),
    games_id INTEGER REFERENCES Games(id)
);

CREATE TABLE IF NOT EXISTS Participation(
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES Athlete(id),
    event_id INTEGER REFERENCES Event(id),
    age INTEGER,
    height INTEGER,
    weight INTEGER,
    medal TEXT CHECK (medal IN ('Gold', 'Silver', 'Bronze', 'NA'))
);

-- \i sql_ddl/vw_cd_sum.sql
-- \i sql_ddl/vw_invest_accounts.sql
-- \i sql_ddl/vw_invest_certificates.sql
-- \i sql_ddl/vw_tdw.sql
-- \i sql_ddl/ddl-customers-001-add.sql
