# Lazarus codex

## A website that lays out information about project lazarus

Project lazarus is a roblox game based on call of duty zombies. I will be pulling information from the Lazarus fandom page however there are some things that I and my friends who play the game wish were available.

This website will:

- Have a introduction homepage with an updates feed and links to project lazarus related pages like the roblox page and the official discord
- A page attached to a database that will list all the weapons in the game and the ability to open a detailed page for each separate weapon and must include how many rounds it will last
- A calculator for the damage dealt by weapons when multiplied by different multipliers

## Project Structure

- **app** folder

  - **static** folder - Files to be served as-is

    - **css** folder
      - **styles.css** - A user stylesheet
    - **images** folder
      - **icon.svg** - Site favicon
      - _other example images_
      - **hero-home.png** - Hero image for home page
    - **js** folder
      - **utils.js** - Utility functions

  - **templates** folder

    - **components** folder
      - **messages.jinja** - Block to display flash messages
      - _other component templates_
    - **pages** folder
      - **base.jinja** - The base template for all pages
      - _other templates for specific pages_

  - **helpers** folder - Utility functions

    - **db.py** - Functions for database access
    - **errors.py** - Functions for error reporting
    - **session.py** - Functions to manage session data
    - **time.py** - Functions to help format timestamps

  - **\_\_init\_\_.py** - App launcher code

- **requirements.txt** - Defines the Python modules needed

- **.env** - Environment variable, e.g. Turso secrets
- **.env-example** - Demo .env file
- **.gitignore** - Prevents venv and .env from being pushed

## Demo Database Schema

The databases used for this website have the following schema:

```sql
CREATE TABLE `weapons` (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT
    'name' TEXT NOT NULL
    'magazineSize' INTEGER NOT NULL
    'totalAmmo' INTEGER NOT NULL
    'damage' INTEGER NOT NULL
    'rpm' INTEGER NOT NULL
    'class' TEXT
    'notes' TEXT
    'price' INTEGER
);

CREATE TABLE `weapons` (
    'id' INTEGER PRIMARY KEY AUTOINCREMENT
    'name' TEXT NOT NULL
    'magazineSize' INTEGER NOT NULL
    'totalAmmo' INTEGER NOT NULL
    'damage' INTEGER NOT NULL
    'rpm' INTEGER NOT NULL
    'baseGun' TEXT
    'module' TEXT
    'notes' TEXT
);


```

## Project Setup and Deployment

See [SETUP.md](SETUP.md) for details of how to install and run the app locally for development, how to setup and configure the [Turso](https://turso.tech/) database, and how to deploy the app to [Render](https://render.com/) for hosting.

## Demo Site

A demo of this site is hosted [here](https://flask-turso-basic-app-setup.onrender.com)

_Note: This is a read-only version to avoid the DB being spammed!_
