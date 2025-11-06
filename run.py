from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from app.models.models import db
from app.routes.auth import auth_bp
from app.routes.appointments import appointments_bp
from flask_migrate import Migrate
from app.routes.root import root_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    JWTManager(app)
    Migrate(app, db)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(appointments_bp, url_prefix='/api')
    app.register_blueprint(root_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)