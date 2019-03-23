import os
import datetime
from flask import abort, Flask, redirect, render_template, request, session
import markdown
import auth
import post

DEFAULT_SERVER_PORT = 5000
HTTP_NOT_FOUND = 404
HTTP_UNAUTHORIZED = 401

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@auth.user_auth
def create():
    errors = None
    header = ""
    signature = ""
    body = ""
    if request.method == "POST":
        header, signature, body, errors = post.validate_form(request)
        if not errors:
            user_uuid = session["user_uuid"]
            post_id = post.create(header, signature, body, user_uuid)
            return redirect("/{}/".format(post_id))
    return render_template(
        "form.html",
        errors=errors,
        header=header,
        signature=signature,
        body=body,
        edit=False
    )


@app.route("/<uuid:post_id>/edit/", methods=["GET", "POST"])
@auth.user_auth
def edit(post_id):
    post_obj = post.read(post_id)
    if not post_obj:
        abort(HTTP_NOT_FOUND)
    if post_obj["user_uuid"] != session["user_uuid"]:
        abort(HTTP_UNAUTHORIZED)
    errors = None
    header = post_obj["header"]
    signature = post_obj["signature"]
    body = post_obj["body"]
    if request.method == "POST":
        header, signature, body, errors = post.validate_form(request)
        if not errors:
            post_id = post.update(post_id, header, signature, body)
            return redirect("/{}/".format(post_id))
    return render_template(
        "form.html",
        errors=errors,
        header=header,
        signature=signature,
        body=body,
        edit=True
    )


@app.route("/<uuid:post_id>/")
@auth.user_auth
def view(post_id):
    post_obj = post.read(post_id)
    if not post_obj:
        abort(HTTP_NOT_FOUND)
    allow_edit = post_obj["user_uuid"] == session["user_uuid"]
    return render_template(
        "post.html",
        post_id=post_id,
        post=post_obj,
        allow_edit=allow_edit
    )


@app.errorhandler(HTTP_NOT_FOUND)
def page_not_found(error):
    return render_template("404.html"), HTTP_NOT_FOUND


@app.template_filter("markdown")
def markdown_filter(text):
    return markdown.markdown(text)


@app.template_filter("datetime")
def datetime_filter(timestamp, date_format="%d-%m-%Y"):
    return datetime.datetime.fromtimestamp(timestamp).strftime(date_format)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", DEFAULT_SERVER_PORT))
    debug = bool(os.environ.get("DEBUG", True))
    app.secret_key = os.environ.get("SECRET_KEY", "debug-key")
    app.run(host="0.0.0.0", debug=debug, port=port)
