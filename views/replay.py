from flask import jsonify, Blueprint
from models import Replay
from web_app import db
import modelsQuery

replay_api = Blueprint('replay_api', __name__)

@replay_api.route('/getAll')
def getAllReplays():
    replays = Replay.query.all()
    return jsonify([i.serialize for i in replays])
