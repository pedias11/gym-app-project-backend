from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from mongoengine import connect
from src.user_blueprint import user
from src.session_blueprint import sessions
from src.admin_blueprint import admin_bp
from flasgger import Swagger

app = Flask(__name__)
jwt = JWTManager(app)

app.config['SWAGGER'] = {
    'title': 'Gym App Project',
    'universion': 3,
}

swagger = Swagger(app)

app.config["JWT_SECRET_KEY"] = "super secret and difficult to guess key"
app.config["SECRET_KEY"] = "another_super_secret_key"

connect(
    host="mongodb+srv://gymuser:4321@cluster0.gnybn7z.mongodb.net",
    db="gym-app-project",
    alias="gym-app-project",
)

cors = CORS(
    app,
    resources={r"*": {"origins": ["http://localhost:4200"]}},
)

app.register_blueprint(user, url_prefix="/user")
app.register_blueprint(sessions, url_prefix="/sessions")
app.register_blueprint(admin_bp, url_prefix="/admin")
