# Third party modules
from flask import jsonify, request, session
from flask_restplus import Namespace, Resource, fields

# First party modules
from app.models import Message, db

api_v1 = Namespace(name="api/v1/")

message_api_model = api_v1.model(
    "Message",
    {
        "id": fields.Integer,
        "content": fields.String,
        "sender_name": fields.String,
        "server_timestamp": fields.String,
    },
)

message_filter_api_model = api_v1.model(
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
        content = data["content"].strip()
        if len(content) == 0:
            return {}
        new_message = Message(
            sender_name=session["username"], content=content
        )
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message)
