from datetime import datetime
from . import db


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    payments = db.relationship("Payment", backref='currency', lazy=True)


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sum = db.Column(db.Float)
    product_description = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
