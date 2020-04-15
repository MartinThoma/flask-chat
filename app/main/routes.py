# Core Library modules
import uuid

# Third party modules
from flask import render_template, session

# First party modules
from app.main import main
from app.models import Message, db


@main.route("/")
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
