import uuid
from functools import wraps
from flask import session


def user_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        user_uuid = session.get("user_uuid")
        if not user_uuid:
            session["user_uuid"] = str(uuid.uuid4())
            session.modified = True
        return func(*args, **kwargs)
    return decorated_function
