
from flask import Flask
from flask_restx import Api

from app.config import Config
from app.database import db
from app.models import migrate_data, User, Order, Offer
from app.views.offers import offer_ns
from app.views.orders import order_ns
from app.views.users import user_ns
from data import users_data, orders_data, offers_data


def create_app(config: Config) -> Flask:
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()
    return application


def configure_app(application: Flask):
    db.init_app(application)
    api = Api()
    api.add_namespace(user_ns)
    api.add_namespace(order_ns)
    api.add_namespace(offer_ns)


if __name__ == '__main__':
    app_config = Config()
    app = create_app(app_config)
    configure_app(app)
    migrate_data(users_data, User)
    migrate_data(orders_data, Order)
    migrate_data(offers_data, Offer)
    app.run()

