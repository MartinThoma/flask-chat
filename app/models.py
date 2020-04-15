# Core Library modules
import datetime

# Third party modules
from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
