from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS, cross_origin

db = SQLAlchemy()
migrate = Migrate()
cors = CORS()

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)
    app.config['CORS_HEADERS'] = 'Content-Type'

    from app.blueprints.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.blueprints.api import bp as api_bp
    app.register_blueprint(api_bp)

    from app.blueprints.database import bp as database_bp
    app.register_blueprint(database_bp)

    return app