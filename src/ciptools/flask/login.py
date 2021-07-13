import functools

import werkzeug.exceptions
from flask import session

from .tools import get_user_name


# this should be put around each web page call. this forces the page to require
# a username in the request headers (e.g. from shibboleth or basic auth)
def require_username(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        username = get_user_name()
        if not username or username == "(null)":
            raise werkzeug.exceptions.Unauthorized("You do not have access to this resource. Please try logging in again.")
        else:
            # this is used by the xhr and websocket endpoints to validate
            # the user without requiring a trip through the idp.
            session["username"] = username
            return f(*args, **kwargs)

    return wrapped


# this should be put around each xhr call. this forces the page to require a
# username in the current session.
def require_session_username(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        username = session.get("username")
        if not username or username == "(null)":
            raise werkzeug.exceptions.Unauthorized("You do not have access to this resource. Please try logging in again.")
        else:
            return f(*args, **kwargs)
    return wrapped


# this should be put around each websocket call. this forces the websocket
# callback to require a username in the current session.
def require_websocket_session(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        username = session.get("username")
        if not username or username == "(null)":
            import flask_socketio
            flask_socketio.disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped
