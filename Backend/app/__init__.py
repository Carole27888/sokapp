from flask import Flask
from app.extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager



migrate = Migrate()  # Instantiate without app

from app.routes.user import user_bp
from app.routes.match import match_bp
from app.routes.user_profile import user_profile_bp
from app.routes.weekly_market_summary import weekly_market_summary_bp
from app.routes.tag_category import tag_category_bp
from app.routes.swipe_action import swipe_action_bp
from app.routes.subscription import subscription_bp
from app.routes.session import session_bp
from app.routes.push_token import push_token_bp
from app.routes.produce_listing import produce_listing_bp
from app.routes.payment import payment_bp
from app.routes.payment_gateway import payment_gateway_bp
from app.routes.order import order_bp
from app.routes.offer import offer_bp
from app.routes.notification import notification_bp
from app.routes.message import message_bp
from app.routes.image import image_bp
from app.routes.geo_location import geo_location_bp
from app.routes.feedback import feedback_bp
from app.routes.export_data import export_data_bp
from app.routes.cms_content import cms_content_bp
from app.routes.bulk_upload import bulk_upload_bp
from app.routes.admin_audit import admin_audit_bp
from app.routes.activity_log import activity_log_bp
from app.routes.pricing_history import pricing_history_bp

jwt = JWTManager()  # Instantiate JWTManager
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['SECRET_KEY'] = 'test'
    app.config['JWT_SECRET_KEY'] = 'test'
    app.config['JWT_TOKEN_LOCATION'] = ['headers']

    db.init_app(app)
    migrate.init_app(app, db)  

    jwt.init_app(app)

    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(match_bp, url_prefix='/api')
    app.register_blueprint(user_profile_bp, url_prefix='/api')
    app.register_blueprint(weekly_market_summary_bp, url_prefix='/api')
    app.register_blueprint(tag_category_bp, url_prefix='/api')
    app.register_blueprint(swipe_action_bp, url_prefix='/api')
    app.register_blueprint(subscription_bp, url_prefix='/api')
    app.register_blueprint(session_bp, url_prefix='/api')
    app.register_blueprint(push_token_bp, url_prefix='/api')
    app.register_blueprint(produce_listing_bp, url_prefix='/api')
    app.register_blueprint(payment_bp, url_prefix='/api')
    app.register_blueprint(payment_gateway_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')
    app.register_blueprint(offer_bp, url_prefix='/api')
    app.register_blueprint(notification_bp, url_prefix='/api')
    app.register_blueprint(message_bp, url_prefix='/api')
    app.register_blueprint(image_bp, url_prefix='/api')
    app.register_blueprint(geo_location_bp, url_prefix='/api')
    app.register_blueprint(feedback_bp, url_prefix='/api')
    app.register_blueprint(export_data_bp, url_prefix='/api')
    app.register_blueprint(cms_content_bp, url_prefix='/api')
    app.register_blueprint(bulk_upload_bp, url_prefix='/api')
    app.register_blueprint(admin_audit_bp, url_prefix='/api')
    app.register_blueprint(activity_log_bp, url_prefix='/api')
    app.register_blueprint(pricing_history_bp, url_prefix='/api')

    return app