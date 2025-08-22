from flask import Blueprint, jsonify

def register_routes(app):
    from src.api.controllers.notifications_controller import bp as notifications_bp
    from src.api.controllers.complaints_controller import bp as complaints_bp
    from src.api.controllers.seed_controller import bp as seed_bp

    app.register_blueprint(notifications_bp)
    app.register_blueprint(complaints_bp)
    app.register_blueprint(seed_bp)

    @app.get("/api/hello")
    def hello():
        return jsonify({"message": "API is up!"})
