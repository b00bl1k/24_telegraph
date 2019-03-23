import uuid
from functools import wraps
from flask import make_response, session


def user_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            session["user_uuid"] = str(uuid.uuid4())
            session.modified = True
        return f(*args, **kwargs)
    return decorated_function
