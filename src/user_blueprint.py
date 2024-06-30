from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import create_access_token
from src.user_model import User
import json
from werkzeug.security import check_password_hash
from flasgger import swag_from


user = Blueprint("user", __name__)

@user.route("/register", methods=["POST"])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'firstname': {'type': 'string'},
                    'lastname': {'type': 'string'},
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['firstname', 'lastname', 'email', 'password']
            }
        }
    ],
    'responses': {
        201: {'description': 'User registered successfully'},
        400: {'description': 'Registration failed'}
    }
})
def register():
    """
    Register a new user.
    """
    try:
        data = request.get_json()
        User(**data).save()
        return Response(json.dumps({"msg": "User registered"}), status=201)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/check_duplicate_email/<string:email>", methods=["GET"])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'email',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Email to check for duplicates'
        }
    ],
    'responses': {
        200: {'description': 'Email available'},
        400: {'description': 'Email already in use'}
    }
})
def check_duplicate_email(email):
    """
    Check if an email is already in use.
    """
    try:
        if User.objects(email=email):
            return Response(json.dumps({"msg": "Email already in use"}), status=400)
        return Response(json.dumps({"msg": "Email available"}), status=200)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/login", methods=["POST"])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'msg': {'type': 'string'},
                    'access_token': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid credentials'
        }
    }
})
def login():
    """Login a user."""
    try:
        data = request.get_json()
        user = User.objects(email=data["email"]).first()
        if user:
            if check_password_hash(user.password, data["password"]):
                fullname = f"{user.firstname}  {user.lastname}"
                identity = {"fullname": fullname, "email": user.email}
                access_token = create_access_token(identity=identity)
                return Response(
                    json.dumps(
                        {"msg": "Login successful", "access_token": access_token}
                    ),
                    status=200,
                )
        return Response(json.dumps({"msg": "Invalid credentials"}), status=400)
    except Exception as e:
        print(e)
        return Response(json.dumps({"msg": str(e)}), status=400)


@user.route("/select_subscription", methods=['POST'])
@swag_from({
    'tags': ['User'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'subscription': {'type': 'string'}
                },
                'required': ['email', 'subscription']
            }
        }
    ],
    'responses': {
        200: {'description': 'Subscription updated successfully'},
        400: {'description': 'User not found'},
        415: {'description': 'Request body must be JSON'}
    }
})
def update_subscription():
    """
    Select user subscription.
    """
    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        subscription = data.get('subscription')

        if not email:
            return jsonify({"msg": "Email is required"}), 400
        user = User.objects(email=email).first()
        
        if user:
            user.update(subscription=subscription)
            user.reload()
            return jsonify({"msg": "Subscription updated successfully"}), 200
        else:
            return jsonify({"msg": "User not found"}), 404
    else:
        return jsonify({"msg": "Request body must be JSON"}), 415        

    