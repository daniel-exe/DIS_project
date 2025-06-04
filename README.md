# Olympic dashboard app
Web-app that can show interesting facts about the Olympics from Athens 1896 to Rio 2016!

Data set:

    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Made by:

    xfm358   Anna Bartholdy Spanggaard
    rjs561 Daniel Nicholas Mølhave

Git repository:

    https://github.com/daniel-exe/DIS_project

## Virtual environment
First navigate to the desired directory and then create virtual environment:

    python3 -m venv venv

Then activate the environment:

    source venv/bin/activate

## Requirements
Run the code below to install the necessary modules:

    pip install -r requirements.txt

## Set up and run the app
### Database initialization
First, ensure that psql is installed (if installed but unavailable, make sure it is added to your shell profile):

    psql --version

#### Set user and password and create database
First create the database:

    createdb -U postgres -h 127.0.0.1 olympics 

Open a psql prompt for the user postgres with host 127.0.0.1:

    psql -U postgres -h 127.0.0.1

Once inside the shell run the following command to set the password for the user postgres:

    ALTER USER postgres WITH PASSWORD '123';

Then quit the shell

    \q

#### Populate the tables
Navigate to the olympics_app folder and run the schema.sql file in your database:

    psql -U postgres -h 127.0.0.1 -d olympics -f schema.sql

Then run the python file load_data.py (it can take a minute...):

    python3 load_data.py

### Run the app
To start the web app run the python file run.py:

    python3 run.py

Then open a web browser and navigate to <http://127.0.0.1:5000>

The web app should now be up and running!


## How to run:
### Database init
1. set the database in __init__.py file.
2. run schema.sql, schema_ins.sql, schema_upd.sql in your database
3. run sql_ddl/ddl-customers-001-add.sql in your database.

Example:

    psql -d olympics -U postgres -W -f schema.sql

#### notes
For Ubuntu add host (-h127.0.0.1) to psql:

    psql -d olympics -U postgres -h127.0.0.1 -W -f schema.sql

#### Change password and db name with postgreSQL on Linux
Open psql

    sudo -u postgres psql

Inside psql shell

    ALTER USER postgres WITH PASSWORD '123';
    CREATE DATABASE olympics;

### Populate the tables

    python3 load_data.py

(it can take a minute...)

### Running flask
#### The python way

    python3 run.py

#### The flask way.

    export FLASK_APP=run.py
    export FLASK_DEBUG=1           (Replaces export FLASK_ENV=development)
    export FLASK_RUN_PORT=5004     (Optional if you want to change port numbe4. Default port is port 5000.)
    flask run

##### notes
For Windows you may have to use the SET command instead of EXPORT. Ex set FLASK_APP=run.py; set FLASK_DEBUG=1; flask run. This worked for me. Also remeber to add the path to your postgres bin-directory in order to run (SQL interpreter) and other postgres programs in any shell.


#### The flask way with a virual environment.

Set up virtual environment as specified in https://flask.palletsprojects.com/en/1.1.x/installation/ (OSX/WINDOWS)
vitualenv may be bundled with python.

##### OSX:

    mkdir myproject
    cd myproject

Create virtual environment in folder

    python3 -m venv .venv

Activate virtual environment in folder

    . .venv/bin/activate

Install flask

    pip install Flask

Set environment variables and start flask

    export FLASK_APP=run.py
    export FLASK_DEBUG=1           (Replaces export FLASK_ENV=development)
    export FLASK_RUN_PORT=5000     (Optional if you want to change port number. Default port is port 5000.)
    flask run


##### WINDOWS:

Create virtual environment in folder

    mkdir myproject
    cd myproject
    py -3 -m venv .venv

Activate virtual environment in folder

    .venv\Script\activate
    pip install Flask

Set environment variables and start flask

    set FLASK_APP=run.py
    set FLASK_DEBUG=1           (Replaces export FLASK_ENV=development)
    set FLASK_RUN_PORT=5000     (Optional if you want to change port number. Default port is port 5000.)
    flask run


## How to use:
