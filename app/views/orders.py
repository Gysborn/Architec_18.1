from app.models import Order
from flask import request
from flask_restx import Resource, Namespace
from app.database import db
from app.models import OrderSchema

order_ns = Namespace('orders')

order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)


@order_ns.route('/')
class OrderView(Resource):
    def get(self):
        order = Order.query.all()
        if not order:
            return "Error", 404
        else:
            return orders_schema.dump(Order)

    def post(self):
        try:
            new_order = request.json
            order = Order(**new_order)
            db.session.add(order)
        except Exception as e:
            return f'Ошибка {e}'

        db.session.commit()
        return "Пользователь добавлен", 204


@order_ns.route('/<int: idx>')
class OrderView(Resource):
    def get(self, idx):
        try:
            order = Order.query.get(idx)
        except Exception as e:
            return f'Error {e}'
        return order_schema.dump(order)

    def put(self, idx):
        try:
            upd_data = request.json
            order = Order.query.get(idx)
            [setattr(order, k, v) for k, v in upd_data.items()]

            db.session.add(order)
        except Exception as e:
            return f'Ошибка {e}'
        db.session.commit()
        return "Данные обновлены", 204

    def delete(self, idx):
        try:
            order = Order.query.get(idx)
            db.session.delete(order)
        except Exception as e:
            return f'Ошибка {e}'
        db.session.commit()
        return 'deleted', 204

