from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
jwt = JWTManager()
socketio = SocketIO()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)
    jwt.init_app(app)
    socketio.init_app(app)
    bcrypt.init_app(app)

    from app.routes import main
    from app.routes.auth import auth
    from app.routes.race import race
    from app.routes.stats import stats
    from app.routes.leaderboard import leaderboard
    app.register_blueprint(main)
    app.register_blueprint(auth)
    app.register_blueprint(race)
    app.register_blueprint(stats)
    app.register_blueprint(leaderboard)

    from app import models
    from app import sockets

    return app