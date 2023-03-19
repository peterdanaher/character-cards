import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, origin):
    """Render message as an apology to user."""
    """ Renders apology template with message and a link to the original site they came from """
    return render_template("apology.html", message=message, origin = origin)

