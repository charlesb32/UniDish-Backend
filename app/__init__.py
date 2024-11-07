from flask import Flask
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from .blueprints.auth import auth_blueprint, init_auth_blueprint
# from .blueprints.dining import dining_blueprint
from .blueprints.posts import posts_blueprint
from .blueprints.statistic_reports import statistic_reports_blueprint

from app.services.database import get_db_connection

from app.controllers.restaurant_controller import RestaurantController
from app.data_access.restaurant_dao import RestaurantDAO
from app.services.restaurant_service import RestaurantService

from app.controllers.dining_hall_controller import DiningHallController
from app.data_access.dining_hall_dao import DiningHallDAO
from app.services.dining_hall_service import DiningHallService

from app.controllers.menu_item_controller import MenuItemController
from app.data_access.menu_item_dao import MenuItemDAO
from app.services.menu_item_service import MenuItemService

from app.controllers.review_controller import ReviewController
from app.data_access.review_dao import ReviewDAO
from app.services.review_service import ReviewService

from app.controllers.comment_controller import CommentController
from app.data_access.comment_dao import CommentDAO
from app.services.comment_service import CommentService

from app.controllers.like_controller import LikeController
from app.data_access.like_dao import LikeDAO
from app.services.like_service import LikeService

def setup_dao(db_connection):
    restaurant_dao = RestaurantDAO(db_connection)
    dining_hall_dao = DiningHallDAO(db_connection)
    menu_item_dao = MenuItemDAO(db_connection)
    review_dao = ReviewDAO(db_connection)
    comment_dao = CommentDAO(db_connection)
    like_dao = LikeDAO(db_connection)
    
    return{
        "restaurant_dao": restaurant_dao,
        "dining_hall_dao": dining_hall_dao,
        "menu_item_dao": menu_item_dao,
        'review_dao': review_dao,
        "comment_dao": comment_dao,
        "like_dao": like_dao
    }

def setup_service(dao_map):
    restaurant_service = RestaurantService(dao_map['restaurant_dao'])
    dining_hall_service = DiningHallService(dao_map["dining_hall_dao"])
    menu_item_service = MenuItemService(dao_map['menu_item_dao'])
    review_service = ReviewService(dao_map['review_dao'])
    comment_service = CommentService(dao_map["comment_dao"])
    like_service = LikeService(dao_map["like_dao"])
    
    return {
        "restaurant_service" : restaurant_service,
        "dining_hall_service" : dining_hall_service,
        "menu_item_service": menu_item_service,
        "review_service": review_service,
        "comment_service": comment_service,
        "like_service": like_service
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

     # Create the controller instance
    restaurant_controller = RestaurantController(service_map['restaurant_service'])
    dining_hall_controller = DiningHallController(service_map["dining_hall_service"])
    menu_item_controller = MenuItemController(service_map['menu_item_service'])
    review_controller = ReviewController(service_map['review_service'])
    comment_controller = CommentController(service_map["comment_service"])
    like_controller = LikeController(service_map["like_service"])
    
    # Register routes by wrapping the instance methods
    app.add_url_rule('/api/restaurants/addRestaurant', 'add_restaurant', lambda: restaurant_controller.add_restaurant(), methods=['POST'])
    app.add_url_rule('/api/restaurants/deleteRestaurant/<int:restaurant_id>', 'delete_restaurant', lambda restaurant_id: restaurant_controller.delete_restaurant(restaurant_id), methods=['DELETE'])
    app.add_url_rule('/api/restaurants/updateRestaurant', 'update_restaurant', lambda: restaurant_controller.edit_restaurant(), methods=['PUT'])
    app.add_url_rule('/api/restaurants/getRestaurant/<int:restaurant_id>', 'get_restaurant', lambda restaurant_id: restaurant_controller.get_restaurant(restaurant_id), methods=['GET'])
    
    app.add_url_rule('/api/diningHalls/addDiningHall', 'add_dining_hall', lambda: dining_hall_controller.add_dining_hall(), methods=['POST'])
    app.add_url_rule('/api/diningHalls/deleteDiningHall/<int:dining_hall_id>', 'delete_dining_hall', lambda dining_hall_id: dining_hall_controller.delete_dining_hall(dining_hall_id), methods=['DELETE'])
    app.add_url_rule('/api/diningHalls/updateDiningHall', 'update_dining_hall', lambda: dining_hall_controller.edit_dining_hall(), methods=['PUT'])
    app.add_url_rule('/api/diningHalls/getDiningHallsWithRestaurants', 'get_dining_halls_with_restaurants', lambda: dining_hall_controller.get_dining_halls_with_restaurants(), methods=["GET"])
    
    app.add_url_rule('/api/menuItems/addMenuItem', 'add_menu_item', lambda: menu_item_controller.add_menu_item(), methods=['POST'])
    app.add_url_rule('/api/menuItems/editMenuItem', 'edit_menu_item', lambda: menu_item_controller.edit_menu_item(), methods=['PUT'])
    app.add_url_rule('/api/menuItems/deleteMenuItem/<int:menu_item_id>', 'delete_menu_item', lambda menu_item_id: menu_item_controller.delete_menu_item(menu_item_id), methods=['DELETE'])
    app.add_url_rule('/api/menuItems/getMenuItemsForRestaurant/<int:restaurant_id>', 'get_menu_items_for_restaurant', lambda restaurant_id: menu_item_controller.get_menu_items_for_restaurant(restaurant_id), methods=['GET'])

    app.add_url_rule('/api/reviews/addReview', 'add_review', lambda: review_controller.add_review(), methods=['POST'])
    
    app.add_url_rule('/api/comments/addComment', 'add_comment', lambda: comment_controller.add_comment(), methods=['POST'])
    
    app.add_url_rule('/api/likes/like', 'like', lambda: like_controller.like(), methods=['POST'])
    
    app.register_blueprint(auth_blueprint)
    # app.register_blueprint(dining_blueprint)
    app.register_blueprint(posts_blueprint)
    app.register_blueprint(statistic_reports_blueprint)
    # app.register_blueprint(dining_hall_blueprint, url_prefix='/api/diningHalls')
    # app.register_blueprint(restaurant_blueprint, url_prefix='/api/restaurants')

    return app
