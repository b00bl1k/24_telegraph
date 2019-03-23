import os
import json
import uuid
import datetime

POSTS_DIR = "posts"


def get_post_filepath(post_id):
    filename = "{}.json".format(post_id)
    filepath = os.path.join(POSTS_DIR, filename)
    return filepath


def save(post_id, post):
    os.makedirs(POSTS_DIR, exist_ok=True)
    filepath = get_post_filepath(post_id)
    with open(filepath, "w") as fh:
        json.dump(post, fh)


def create(header, signature, body, user_uuid):
    post_id = str(uuid.uuid4())
    cur_timestamp = int(datetime.datetime.now().timestamp())
    post = {
        "created_at": cur_timestamp,
        "updated_at": cur_timestamp,
        "user_uuid": user_uuid,
        "header": header,
        "signature": signature,
        "body": body
    }
    save(post_id, post)
    return post_id


def update(post_id, header, signature, body):
    post = read(post_id)
    if not post:
        return None
    cur_timestamp = int(datetime.datetime.now().timestamp())
    post["updated_at"] = cur_timestamp
    post["header"] = header
    post["signature"] = signature
    post["body"] = body
    save(post_id, post)
    return post_id


def read(post_id):
    filepath = get_post_filepath(post_id)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r") as fh:
        return json.load(fh)


def validate_form(request):
    errors = []
    header = request.form["header"].strip()
    signature = request.form["signature"].strip()
    body = request.form["body"].strip()
    if not header:
        errors.append("The 'header' field is required")
    if len(header) > 255:
        errors.append("The 'header' field is longer than 255 symbols")
    if len(signature) > 255:
        errors.append("The 'signature' field is longer than 255 symbols")
    if not body:
        errors.append("The 'body' field is required")
    if len(body) > 4096:
        errors.append("The 'body' field is longer than 4096 symbols")
    return header, signature, body, errors
