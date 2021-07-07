from random import randint
from faker import Faker
from . import db
from .models import Currency, Payment


def currency():
    for i in ["EUR", "USD", "RUB"]:
        currency = Currency(name=i)
        db.session.add(currency)
    db.session.commit()

def payments(count=30):
    fake = Faker()
    currencies = Currency.query.all()
    for i in range(count):
        payment = Payment(
                    sum=randint(1, 1000),
                    product_description=fake.text(
                        max_nb_chars=400
                    ),
                    timestamp=fake.past_date(),
                    currency=currencies[randint(0, 2)]
                )
        db.session.add(payment)
    db.session.commit()


def main():
    currency()
    payments()
    print("Success")