import functools
import json

import flask
from ciptools.validators import ValidationError


def validate_request_data(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # make sure that we were given a request body
        if not flask.request.data:
            raise ValidationError("Empty data received.")

        # make sure that it is valid utf8 data
        try:
            data = flask.request.data.decode("utf8")
        except UnicodeDecodeError:
            raise ValidationError("Non-UTF8 data received that could not be decoded.")

        # make sure that it is valid json
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValidationError("Non-JSON data received that could not be parsed.")

        flask.request.data = data
        return f(*args, **kwargs)

    return wrapped
