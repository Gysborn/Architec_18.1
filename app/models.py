from app.database import db
from marshmallow import Schema, fields


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    role = db.Column(db.String(30))
    phone = db.Column(db.String(20))
    as_executor_in_offers = db.relationship('Offer', foreign_keys='Offer.executor_id')  # Положит список всех оферов
    # в которых он указан как исполнитель
    as_executor_in_orders = db.relationship('Order', foreign_keys='Order.executor_id')
    as_customer_in_orders = db.relationship('Order', foreign_keys='Order.customer_id')


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    first_name = fields.Str()
    last_name = fields.Str()
    age = fields.Int()
    email = fields.Str()
    role = fields.Str()
    phone = fields.Int()


class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    description = db.Column(db.String(255))
    start_date = db.Column(db.String(255))
    end_date = db.Column(db.String(255))
    address = db.Column(db.String(255))
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey(User.id))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    as_order_in_offers = db.relationship('Offer')  # Ищет в Офере внешний ключ ссылающийся

    # на него самого и кладет в переменную


class OrderSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    description = fields.Str()
    start_date = fields.Str()
    end_date = fields.Str()
    address = fields.Str()
    price = fields.Int()
    customer_id = fields.Pluck(UserSchema, 'id')
    executor_id = fields.Pluck(UserSchema, 'id')


class Offer(db.Model):
    __tablename__ = "offers"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey(User.id))

    order = db.relationship('Order', back_populates="as_order_in_offers", foreign_keys=[order_id])  # кладет экз. заказа
    # на который ссылается внешний ключ
    # order_id(as_order_in_offers)
    executor = db.relationship('User', back_populates="as_executor_in_offers", foreign_keys=[executor_id])  #


class OfferSchema(Schema):
    id = fields.Int(dump_only=True)
    order_id = fields.Pluck(OrderSchema, 'id')
    executor_id = fields.Pluck(UserSchema, 'id')


def migrate_data(data, model):
    try:
        for d in data:
            new_inst = model(**d)
            db.session.add(new_inst)

    except Exception as e:
        print(f'Ощибочка вышла {e}')
    db.create_all()
    db.session.commit()
