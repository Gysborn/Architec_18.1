from flask import request
from flask_restx import Resource, Namespace
from app.database import db
from app.models import UserSchema, User

user_ns = Namespace('users')

user_schema = UserSchema()
users_schema = UserSchema(many=True)


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        user = User.query.all()
        # if not user:
        #     return "Error", 404
        # else:
        return users_schema.dump(user)

    def post(self):
        try:
            new_user = request.json
            user = User(**new_user)
            db.session.add(user)
        except Exception as e:
            return f'Ошибка {e}'

        db.session.commit()
        return "Пользователь добавлен", 204


@user_ns.route('/<int: idx>')
class UserView(Resource):
    def get(self, idx):
        try:
            user = User.query.get(idx)
        except Exception as e:
            return f'Error {e}'
        return user_schema.dump(user)

    def put(self, idx):
        try:
            upd_user = request.json
            user = User.query.get(idx)
            [setattr(user, k, v) for k, v in upd_user.items()]

            db.session.add(user)

        except Exception as e:
            return f'Ошибка {e}'

        db.session.commit()
        return f"Данные обновлены", 204

    def delete(self, idx):
        try:
            user = User.query.get(idx)
            db.session.delete(user)
        except Exception as e:
            return f'Ошибка {e}'
        db.session.commit()
        return 'deleted', 204
