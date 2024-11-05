from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .blueprints.auth import auth_blueprint, init_auth_blueprint
from .blueprints.dining import dining_blueprint
from .blueprints.posts import posts_blueprint
from .blueprints.statistic_reports import statistic_reports_blueprint
from .controllers.dining_hall_controller import dining_hall_blueprint
from .controllers.restaurant_controller import RestaurantController, restaurant_blueprint
from app.services.database import get_db_connection
from app.data_access.restaurant_dao import RestaurantDAO
from app.services.restaurant_service import RestaurantService
# from app.controllers.restaurant_controller import RestaurantController

def setup_dao(db_connection):
    restaurant_dao = RestaurantDAO(db_connection)
    return{
        "restaurant_dao": restaurant_dao,
    }

def setup_service(dao_map):
    restaurant_service = RestaurantService(dao_map['restaurant_dao'])
    return {
        "restaurant_service" : restaurant_service,
    }
def create_app():
    app = Flask(__name__)
    CORS(app)  
    app.config['JWT_SECRET_KEY'] = 'SECRET_KEY'  # Better to use environment variables
    bcrypt = Bcrypt(app)
    jwt_manager = JWTManager(app)
    # Initialize auth_blueprint with bcrypt
    init_auth_blueprint(bcrypt)
    # Set up the database connection
    db = get_db_connection()
    dao_map = setup_dao(db)
    service_map = setup_service(dao_map)
    # restaurant_controller = RestaurantController(service_map['restaurant_service'])
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dining_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(statistic_reports_blueprint)
    app.register_blueprint(dining_hall_blueprint, url_prefix='/api/diningHalls')
    app.register_blueprint(restaurant_blueprint, url_prefix='/api/restaurants')

    return app
