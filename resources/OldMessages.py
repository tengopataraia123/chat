from flask_restful import Resource, reqparse
from database import MessageModel
import json

class OldMessageFetcher(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument("room",type=str,required=True,help="Porvide room")

    def get(self):
        data = OldMessageFetcher.parser.parse_args()
        messages = MessageModel.getMessages(data["room"])
        return json.dumps({"messageList":messages})