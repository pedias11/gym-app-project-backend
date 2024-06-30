from flask import Blueprint, jsonify, request, Response
from src.session_model import UserSessionItem
import json
from bson import json_util
from flasgger import swag_from

sessions = Blueprint("sessions", __name__)

def session_to_dict(session):
    return {
        "_id": str(session.id),
        "email": session.email,
        "date": session.date,
        "time": session.time
    }

def mongo_to_json(document):
    return json.loads(json_util.dumps(document))


@sessions.route("/add_session", methods=["POST"])
@swag_from({
    'tags': ['Sessions'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'date': {'type': 'string', 'format': 'date'},
                    'time': {'type': 'string'}
                },
                'required': ['email', 'date', 'time']
            }
        }
    ],
    'responses': {
        201: {'description': 'Session added'},
        400: {'description': 'Failed to add session'}
    }
})
def add_session():
    """
    Add a new session.
    """
    try:
        data = request.get_json()
        UserSessionItem(**data).save()
        return Response(json.dumps({"msg": "Session added"}), status=201)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)



@sessions.route("/email/<string:email>", methods=["GET"])
@swag_from({
    'tags': ['Sessions'],
    'parameters': [
        {
            'name': 'email',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Email to retrieve sessions for'
        }
    ],
    'responses': {
        200: {
            'description': 'Sessions retrieved successfully',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        '_id': {'type': 'string'},
                        'email': {'type': 'string'},
                        'date': {'type': 'string', 'format': 'date'},
                        'time': {'type': 'string'}
                    }
                }
            }
        },
        404: {'description': 'Sessions not found'},
        400: {'description': 'Error retrieving sessions'}
    }
})
def get_sessions_by_email(email):
    """
    Get all the sessions for a specific user-email.
    """
    try:
        sessions = UserSessionItem.objects(email=email)
        if sessions:
            session_dicts = [session_to_dict(session) for session in sessions]
            return Response(json.dumps(session_dicts), status=200, mimetype='application/json')
        return Response(json.dumps({"msg": "Sessions not found"}), status=404, mimetype='application/json')
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400, mimetype='application/json')
    

@sessions.route("/delete_last_session_by_email/<string:email>", methods=["DELETE"])
@swag_from({
    'tags': ['Sessions'],
    'parameters': [
        {
            'name': 'email',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Email to delete the last session for'
        }
    ],
    'responses': {
        200: {'description': 'Session deleted successfully'},
        404: {'description': 'No sessions found for the user'},
        400: {'description': 'Error deleting session'}
    }
})
def delete_last_session_by_email(email):
    """
    Delete the last session of a specific user-email.
    """
    try:
        session = UserSessionItem.objects(email=email).order_by('-date').first()
        if session:
            session_date = session.date
            session.delete()
            return jsonify({"msg": f"Session on {session_date} deleted successfully"}), 200
        return jsonify({"msg": "No sessions found for the user"}), 404
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
    
   