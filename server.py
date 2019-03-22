import os
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def form():
    return render_template("form.html")


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)
