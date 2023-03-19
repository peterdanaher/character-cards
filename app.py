""" I used the app.py file from Finance to create the skeleton for this app.py file """
import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, json
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from random import randrange

from helpers import login_required, apology

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///characters.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        """ This origin is passed into the apology template so that it can create a link to return to this page """
        origin = "/login"

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", origin)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", origin)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", origin)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        origin = "/register"

        if not request.form.get("username"):
            return apology("must provide username", origin)

        if not request.form.get("password"):
            return apology("must provide password", origin)

        if (not request.form.get("confirmation")) or request.form.get("confirmation") != request.form.get("password"):
            return apology("Passwords must match", origin)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 0:
            return apology("Username is already taken", origin)

        db.execute("INSERT INTO users (username, hash) VALUES(?,?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        return redirect("/login")

    else:
        return render_template("register.html")


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():

    origin = "/password"

    """Change Password"""
    if request.method == "POST":
        if not request.form.get("password"):
            return apology("Must provide old password", origin)

        rows = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Incorrect password", origin)

        if not request.form.get("new_password"):
            return apology("Must provide new password", origin)
        new_password = request.form.get("new_password")

        if (not request.form.get("confirm_new_password")) or request.form.get("confirm_new_password") != new_password:
            return apology("New passwords must match", origin)

        db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(new_password), session["user_id"])

        return redirect("/logout")

    else:
        return render_template("password.html")


@app.route("/review", methods={"GET"})
@login_required
def review():
    """ Gets data from user table """
    user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
    number_seen = int(user["number_seen"])
    """ If the user does not know any words, they cannot review so they are made to learn new words """
    if number_seen == 0:
        return redirect("/learn")
    level = int(user["difficulty"])
    """ If the user has seen less than level + 5, they will only be shown the number they've seen. 1 is subtracted to account for the starting word """
    number = min(number_seen, 5 + level) - 1

    """ https://www.w3schools.com/sql/sql_join_left.asp I used this as a resource for LEFT JOIN in SQL """
    """ Finds all the words that the user has seen so far, adjoins any notes, and capitalizes """
    characters = db.execute("SELECT * FROM characters LEFT JOIN notes ON characters.id = notes.character_id WHERE characters.id <= ? AND notes.user_id = ?", number_seen, session["user_id"])
    for row in characters:
        row['meaning'] = row['meaning'].capitalize()
        row['pronunciation'] = row['pronunciation'].capitalize()
    """ https://www.geeksforgeeks.org/random-numbers-in-python/ randrange() """
    """ Picks a random index to start with """
    start = randrange(number_seen)

    """ https://medium.com/@crawftv/javascript-jinja-flask-b0ebfdb406b3 How to pass Python objects to Javascript through Jinja """
    j_characters = json.dumps(characters)
    return render_template("review.html", characters = characters, number = number, j_characters = j_characters, start=start, number_seen = number_seen)

@app.route("/difficulty", methods={"GET", "POST"})
@login_required
def difficulty():
    """ If this form is submitted it will change the difficulty to the desired level in the database """
    if request.method == "POST":
        difficulty = request.form.get("difficulty_level")
        db.execute("UPDATE users SET difficulty = ? WHERE id = ?", difficulty, session["user_id"])
        return render_template("index.html")
    else:
        """ Creates the difficulty form and sets the current difficulty to the default option """
        level = int(db.execute("SELECT difficulty FROM users WHERE id = ?", session["user_id"])[0]["difficulty"])
        range = [5, 7, 10]
        options = {5: "easy", 7: "normal", 10: "hard"}
        return render_template("difficulty.html", level = level, range = range, options = options)

@app.route("/learn", methods={"GET", "POST"})
@login_required
def learn():
    """ Max number of characters one could learn """
    max = len(db.execute("SELECT * FROM characters"))
    if request.method == "POST":
        """ Updates the number seen for a user by the amount they have just seen and creates a blank note for each new word """
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        number_seen = int(user["number_seen"])
        level = int(user["difficulty"])
        new_number = min(max, number_seen + level)
        db.execute("UPDATE users SET number_seen = ? WHERE id = ?", new_number, session["user_id"])
        cap = min(level, max - number_seen)
        for i in range(cap):
            db.execute("INSERT INTO notes (character_id, user_id) VALUES(?, ?)", number_seen + i + 1, session["user_id"])
        return render_template("index.html")
    else:
        """ If the user has no more to learn, they are made to review. Otherwise, they are shown characters according to their difficulty. """
        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]
        number_seen = int(user["number_seen"])
        level = int(user["difficulty"])
        if number_seen >= max:
            return redirect("/review")
        characters = db.execute("SELECT * FROM characters WHERE id > ? AND id <= ?", number_seen, number_seen + level)
        for row in characters:
            row["meaning"] = row["meaning"].capitalize()
            row["pronunciation"] = row["pronunciation"].capitalize()
        j_characters = json.dumps(characters)
        return render_template("learn.html", characters = characters, j_characters = j_characters)


@app.route("/notes", methods={"GET", "POST"})
@login_required
def notes():

    origin = "/notes"

    if request.method == "POST":
        """ Searches the database for the desired character and if it is found, it passes it into the add note template """
        if not request.form.get("query"):
            return apology("Must provide search query", origin)
        query = request.form.get("query")
        type = request.form.get("type")
        number_seen = int(db.execute("SELECT number_seen FROM users WHERE id = ?", session["user_id"])[0]["number_seen"])
        if type == "meaning":
            results = db.execute("SELECT * FROM characters WHERE meaning = ? AND id <= ?", query, number_seen)
        else:
            results = db.execute("SELECT * FROM characters WHERE character = ? AND id <= ?", query, number_seen)
        if len(results) != 1:
            return apology("No results found", origin)
        character = results[0]
        character["meaning"] = character["meaning"].capitalize()
        character["pronunciation"] = character["pronunciation"].capitalize()
        return render_template("add_note.html", character = character)
    else:
        return render_template("notes.html")


@app.route("/add_note", methods={"POST"})
@login_required
def add_note():
    """ Once a new is submitted, it updates the note for the user on that specific character in the database """
    if request.form.get("note"):
        note = request.form.get("note")
        character_id = request.form.get("character_id")
        db.execute("UPDATE notes SET note = ? WHERE user_id = ? AND character_id = ?", note, session["user_id"], character_id)
    return render_template("index.html")
