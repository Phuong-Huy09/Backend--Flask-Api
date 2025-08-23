from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from src.config.settings import Config
from src.infrastructure.databases.db import db
from src.api.routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    Migrate(app, db)

    with app.app_context():
        from src.infrastructure.models.user import User  # noqa
        from src.infrastructure.models.notification import Notification  # noqa
        from src.infrastructure.models.complaint import Complaint  # noqa
        db.create_all()

    register_routes(app)
    return app

# Allow: python -m src.create_app
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
