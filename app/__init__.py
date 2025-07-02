#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect
import html
import math

from app.helpers.session import init_session
from app.helpers.db      import connect_db
from app.helpers.errors  import init_error, not_found_error
from app.helpers.logging import init_logging
from app.helpers.time    import init_datetime, utc_timestamp, utc_timestamp_now


# Create the app
app = Flask(__name__)

# Configure app
init_session(app)   # Setup a session for messages, etc.
init_logging(app)   # Log requests
init_error(app)     # Handle errors and exceptions
init_datetime(app)  # Handle UTC dates in timestamps


#-----------------------------------------------------------
# Home page route
#-----------------------------------------------------------
@app.get("/")
def index():
    return render_template("pages/home.jinja")



#-----------------------------------------------------------
# Things page route - Show all the things, and new thing form
#-----------------------------------------------------------
@app.get("/weapons/")
def show_all_things():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, image, class FROM weapons ORDER BY id ASC"
        params = []
        result = client.execute(sql, params)
        weapons = result.rows

        # And show them on the page
        return render_template("pages/baseWeapons.jinja", weapons=weapons)


#-----------------------------------------------------------
# Thing page route - Show details of a single thing
#-----------------------------------------------------------
@app.get("/weapon/<int:id>")
def show_one_thing(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT id, name, price, magazineSize, totalAmmo, damage, rpm, notes, price, image FROM weapons WHERE id=?"
        params = [id]
        result = client.execute(sql, params)
        weapons = result.rows
        # Did we get a result?
        if result.rows:
            # yes, so show it on the page
            weapon = result.rows[0]
            return render_template("pages/weapon.jinja", weapon=weapon)

        else:
            # No, so show error
            return not_found_error()


#-----------------------------------------------------------
# Calculator page
# Major help from AI here not proud of that but I did what I can to make it my own and understand how it works
#-----------------------------------------------------------

@app.route('/calculator', methods=['GET', 'POST'])
def showCalculator():
    result = None
    error = None

    if request.method == 'POST':
        weapon_name = request.form.get('weapon_name', '').strip()
        double_tap = request.form.get('double_tap') == 'on'
        
        with connect_db() as client:
            sql = "SELECT name, damage, headshotMultiplier FROM weapons WHERE LOWER(name) = LOWER(?)"
            params = (weapon_name,)
            result = client.execute(sql, params)
            weapon = result.rows if hasattr(result, 'rows') else []
            # print(f"weapon type: {type(weapon)}") # debugging
            # print(f"weapon result: {weapon}") # debugging
        if weapon:
            damage = weapon[0]['damage']
            headshotMultiplier = weapon[0]['headshotMultiplier']
            result = max_one_shot_round(damage, double_tap, headshotMultiplier)
        else:
            error = f"Weapon '{weapon_name}' not found in database."

    return render_template('pages/calculator.jinja', result=result, error=error)
#---- Function to calculate the max round a gun can reach -------------------------------------------------------
def max_one_shot_round(damage, double_tap,  headshotMultiplier ):
    effective_damage =(damage * (2 if double_tap else 1) * headshotMultiplier)
    print(damage, effective_damage, double_tap, headshotMultiplier)
    if effective_damage < 50:
        return 0
    if effective_damage <= 1050:
        return int(round((effective_damage - 50) / 100))
    else:
        return int(round((math.log(effective_damage / 950)) / math.log(1.1) + 9, 0))










