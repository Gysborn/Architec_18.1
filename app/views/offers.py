from flask import request
from flask_restx import Resource, Namespace
from app.database import db
from app.models import OfferSchema, Offer

offer_ns = Namespace('offers')

offer_schema = OfferSchema()
offers_schema = OfferSchema(many=True)


@offer_ns.route('/')
class OfferView(Resource):
    def get(self):
        offer = Offer.query.all()
        if not offer:
            return "Error", 404
        else:
            return offers_schema.dump(offer)

    def post(self):
        try:
            new_offer = request.json
            offer = Offer(**new_offer)
            db.session.add(offer)
        except Exception as e:
            return f'Ошибка {e}'

        db.session.commit()
        return "Пользователь добавлен", 204


@offer_ns.route('/<int: idx>')
class OfferView(Resource):
    def get(self, idx):
        try:
            offer = Offer.query.get(idx)
        except Exception as e:
            return f'Error {e}'
        return offer_schema.dump(offer)

    def put(self, idx):
        try:
            upd_data = request.json
            offer = Offer.query.get(idx)
            [setattr(offer, k, v) for k, v in upd_data.items()]

            db.session.add(offer)
        except Exception as e:
            return f'Ошибка {e}'
        db.session.commit()
        return "Данные обновлены", 204

    def delete(self, idx):
        try:
            offer = Offer.query.get(idx)
            db.session.delete(offer)
        except Exception as e:
            return f'Ошибка {e}'
        db.session.commit()
        return 'deleted', 204
