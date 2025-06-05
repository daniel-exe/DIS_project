# Olympic dashboard app
Web-app that can show interesting facts about the Olympics from Athens 1896 to Rio 2016!

Data set:

    https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results

Made by:

    xfm358 Anna Bartholdy Spanggaard
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

The web app should now be up and running. The landing page gives
an overview of the features and how to use the web app. Enjoy!


#### How to change password and db name with postgreSQL on Linux
Open psql

    sudo -u postgres psql

Inside psql shell

    ALTER USER postgres WITH PASSWORD '123';
    CREATE DATABASE olympics;

