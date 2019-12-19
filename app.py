#!/usr/bin/python
# coding: utf-8

"""A simple server for a chat application."""

# Core Library
import uuid

# Third party
from flask import Flask, session, render_template
from flask_migrate import Migrate
from flask_restplus import Api

# First party
from api import api_v1
from models import Message, db

app = Flask(__name__)
app.config["SECRET_KEY"] = "689ceeef-9525-4721-be8d-4ff192910eb5"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def entry_point():
    if "username" not in session:
        session["username"] = str(uuid.uuid4())
    messages = Message.query.all()
    last_seen_id = max((message.id for message in messages), default=0)
    return render_template(
        "index.html",
        messages=messages,
        user_id=session["username"],
        last_seen_id=last_seen_id,
    )


migrate = Migrate()

api_base = Api(version="1.0", doc="/swagger/")
api_base.add_namespace(api_v1)

db.init_app(app)
migrate.init_app(app, db)
api_base.init_app(app)


if __name__ == "__main__":
    app.run(debug=True)
