from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .blueprints.auth import auth_blueprint, init_auth_blueprint
from .blueprints.dining import dining_blueprint
from .blueprints.posts import posts_blueprint
from .blueprints.statistic_reports import statistic_reports_blueprint
from .controllers.dining_hall_controller import dining_hall_blueprint
from .controllers.restaurant_controller import restaurant_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)  
    app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'  # Better to use environment variables
    bcrypt = Bcrypt(app)
    jwt_manager = JWTManager(app)
    # Initialize auth_blueprint with bcrypt
    init_auth_blueprint(bcrypt)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dining_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(statistic_reports_blueprint)
    app.register_blueprint(dining_hall_blueprint, url_prefix='/api/diningHalls')
    app.register_blueprint(restaurant_blueprint, url_prefix='/api/restaurants')
    return app
