#===========================================================
# App Creation and Launch
#===========================================================

from flask import Flask, render_template, request, flash, redirect, jsonify
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
def show_all_weapons():
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
def show_one_weapon(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT id, name, price, magazineSize, totalAmmo, damage, rpm, notes, price, image, gamepass FROM weapons WHERE id=?"
        params = [id]
        result = client.execute(sql, params)
        weapons = result.rows
        if result.rows:
            weapon = result.rows[0]
            gamepass = "is" if weapon['gamepass'] == 1 else "not"
            return render_template("pages/weapon.jinja", weapon=weapon, gamepass=gamepass)
        

        else:
            # No, so show error
            return not_found_error()

@app.get("/upgradedWeapon/<int:id>")
def show_one_packed_weapon(id):
    with connect_db() as client:
        # Get the thing details from the DB
        sql = "SELECT * FROM packedWeapons WHERE baseWeaponId = ?"
        params = [id]
        result = client.execute(sql, params)
        weapon = result.rows
        if result.rows:
            weapon = result.rows[0]
            return render_template("pages/packedWeapon.jinja", weapon=weapon)
        

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
        weapon = []
        if weapon_name:
            with connect_db() as client:
                # Try to find the weapon in packedWeapons first
                sql_packed = "SELECT packedName AS name, damage, headshotMultiplier, extraDamage FROM packedWeapons WHERE LOWER(packedName) = LOWER(?)"
                params = [weapon_name]
                result_packed = client.execute(sql_packed, params)
                if hasattr(result_packed, 'rows') and result_packed.rows:
                    weapon = result_packed.rows
                else:
                    # If not found in packedWeapons, try weapons table
                    sql_base = "SELECT name, damage, headshotMultiplier, extraDamage FROM weapons WHERE LOWER(name) = LOWER(?)"
                    result_base = client.execute(sql_base, params)
                    if hasattr(result_base, 'rows'):
                        weapon = result_base.rows

            if weapon:
                damage = weapon[0]['damage']
                headshotMultiplier = weapon[0]['headshotMultiplier']
                extraDamage = weapon[0]['extraDamage']
                result = max_one_shot_round(damage, double_tap, headshotMultiplier, extraDamage)
            else:
                error = f"Weapon '{weapon_name}' not found in weapon database."
        else:
            error = "Please enter a weapon name."

    return render_template('pages/calculator.jinja', result=result, error=error)
#---- Function to calculate the max round a gun can reach -------------------------------------------------------
def max_one_shot_round(damage, double_tap,  headshotMultiplier,extraDamage ):
    effective_damage =((damage + extraDamage) * (2 if double_tap else 1) * headshotMultiplier )
    # print(damage, effective_damage, double_tap, headshotMultiplier)
    if effective_damage < 50:
        return 0
    if effective_damage <= 1050:
        return int(round((effective_damage - 50) / 100))
    else:
        return int(round((math.log(effective_damage / 950)) / math.log(1.1) + 9, 0))


#---- Function to calculate the max round a gun can reach -------------------------------------------------------
@app.get("/autocomplete")
def autocomplete_weapon_names():
    query = request.args.get("query", "").strip().lower()

    if not query:
        return jsonify([])

    weapon_names = []

    with connect_db() as client:
        # Get base weapon names
        sql_base = """
        SELECT name FROM weapons 
        WHERE LOWER(name) LIKE ?
        """
        params = [f"{query}%"]
        result_base = client.execute(sql_base, params)
        weapon_names += [row["name"] for row in result_base.rows]

        # Get packed weapon names
        sql_packed = """
        SELECT packedName FROM packedWeapons
        WHERE LOWER(packedName) LIKE ?
        """
        result_packed = client.execute(sql_packed, params)
        weapon_names += [row["packedName"] for row in result_packed.rows]

    # Remove duplicates and sort
    weapon_names = sorted(list(set(weapon_names)))[:10]

    return jsonify(weapon_names)
#-----------------------------------------------------------
# perks page

#-----------------------------------------------------------

@app.get("/perks/")
def show_all_perks():
    with connect_db() as client:
        # Get all the things from the DB
        sql = "SELECT id, name, price, description, icon, machine FROM perks ORDER BY id ASC"
        params = []
        result = client.execute(sql, params)
        perks = result.rows

        # And show them on the page
        return render_template("pages/perks.jinja", perks=perks)
    







