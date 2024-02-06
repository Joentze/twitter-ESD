"""MIDDLEWARE FOR AUTHORISATION"""
from functools import wraps
from flask import redirect, session, url_for


def requires_auth(f):
    """
    Use on routes that require a valid session, otherwise it aborts with a 403
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.login'))

        return f(*args, **kwargs)

    return decorated
