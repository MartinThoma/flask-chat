#!/usr/bin/python
# coding: utf-8

"""
A simple server for a chat application.

This does NOT include:

* User names / authentication
* Loading only parts of the complete chat log
* Editing of chat massages
* Search
"""

# Core Library
import uuid
import datetime

# Third party
from flask import (
    Flask,
    jsonify,
    request,
    session,
    url_for,
    redirect,
    render_template,
)
from dataclasses import dataclass
from flask_migrate import Migrate
from flask_restplus import Api, Resource, Namespace, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "689ceeef-9525-4721-be8d-4ff192910eb5"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def entry_point():
    if "username" not in session:
        session["username"] = str(uuid.uuid4())
    messages = Message.query.all()
    last_seen_id = max(message.id for message in messages)
    return render_template(
        "index.html",
        messages=messages,
        user_id=session["username"],
        last_seen_id=last_seen_id,
    )


@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("static", path)


db = SQLAlchemy()
migrate = Migrate()

api_base = Api(version="1.0", doc="/swagger/")
api_v1 = Namespace(name="api/v1/")
api_base.add_namespace(api_v1)

db.init_app(app)
migrate.init_app(app, db)
api_base.init_app(app)


@dataclass
class Message(db.Model):
    id: str = db.Column(db.Integer, primary_key=True)
    sender_name: str = db.Column(db.String(255))
    content: str = db.Column(db.Text)
    server_timestamp: datetime.datetime = db.Column(
        db.DateTime, default=datetime.datetime.utcnow
    )

    def __init__(self, sender_name, content, server_timestamp=None):
        self.sender_name = sender_name
        self.content = content
        self.server_timestamp = server_timestamp


message_api_model = api_base.model(
    "Message",
    {
        "id": fields.Integer,
        "content": fields.String,
        "sender_name": fields.String,
        "server_timestamp": fields.String,
    },
)

message_filter_api_model = api_base.model(
    "MessageFilters", {"id": fields.Integer,}
)


@api_v1.route("/messages")
class MessageEndpoint(Resource):
    @api_v1.param("last_seen_id", "The client wants newer messages than that")
    @api_v1.marshal_with(message_api_model, as_list=False)
    def get(self):
        last_seen_id = request.args.get("last_seen_id", 0)
        messages = Message.query.filter(Message.id > last_seen_id).all()
        return messages

    @api_v1.expect(message_api_model, validate=True)
    def post(self):
        data = request.json
        new_message = Message(
            sender_name=session["username"], content=data["content"]
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message)


if __name__ == "__main__":
    app.run(debug=True)
