import hashlib
import requests
from flask import render_template, redirect, url_for, flash, request,\
    current_app
from . import main
from .. import db
from .forms import PaymentForm
from ..models import Payment, Currency


@main.route('/', methods=['GET', 'POST'])
def index():
    form=PaymentForm()
    if form.validate_on_submit():
        currency = Currency.query.get(form.currency.data)
        new_payment = Payment(
            sum = form.sum.data,
            product_description = form.product_description.data,
            currency = currency
        )

        db.session.add(new_payment)
        db.session.commit()

        if currency.name == "EUR":
            return redirect(url_for('main.pay', payment_id=new_payment.id))
        elif currency.name == "USD":
            return redirect(url_for('main.advcash', payment_id=new_payment.id))
        elif currency.name == "RUB":
            return redirect(url_for('main.invoice', payment_id=new_payment.id))
        return redirect(url_for('main.index'))

    page = request.args.get('page', 1, type=int)
    pagination = Payment.query.order_by(Payment.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POST_PER_PAGE'],
        error_out=False)
    payments = pagination.items
    return render_template('index.html', form=form, payments=payments, pagination=pagination)


@main.route('/pay', methods=['GET', 'POST'])
def pay():
    shop_id = current_app.config["SHOP_ID"]
    secret_key = current_app.config["SECRET_KEY"]
    payment = Payment.query.get(request.args["payment_id"])
    # EUR currency code = 978
    # this page for pay in EUR
    code_currency = 978

    text = (
        ":".join([
            str(payment.sum),
            str(code_currency),
            str(shop_id),
            str(payment.id)
        ])
    ) + secret_key
    SignatureValue = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()  # amount:currency:shop_id:shop_order_idsecret_key
    return render_template('pay.html', shop_id=shop_id, SignatureValue=SignatureValue, code_currency=code_currency, payment=payment)


@main.route('/advcash', methods=['GET', 'POST'])
def advcash():
    shop_id = current_app.config["SHOP_ID"]
    secret_key = current_app.config["SECRET_KEY"]
    payment = Payment.query.get(request.args["payment_id"])
    # USD currency code = 840
    # this page for pay in USD
    payer_currency = 840
    shop_currency = current_app.config["SHOP_CURRENCY"]

    text = (
        ":".join([
            str(payer_currency),
            str(payment.sum),
            str(shop_currency),
            str(shop_id),
            str(payment.id),
        ])
    ) + secret_key
    SignatureValue = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()  # payer_currency:amount:shop_currency:shop_id:shop_order_idsecret_key

    pay_request = requests.post(
        'https://core.piastrix.com/bill/create',
        json={
            "description": payment.product_description,
            "payer_currency": payer_currency,
            "shop_amount": payment.sum,
            "shop_currency": shop_currency,
            "shop_id": shop_id,
            "shop_order_id": payment.id,
            "sign": SignatureValue,
        }
    )

    dict_response = pay_request.json()
    # if response == none
    if not dict_response["data"]:
        db.session.delete(payment)
        db.session.commit()
        flash(f"Error: {dict_response['message']}")
        return redirect(url_for('main.index'))

    return redirect(dict_response["data"]["url"])


@main.route('/invoice', methods=['GET', 'POST'])
def invoice():
    shop_id = current_app.config["SHOP_ID"]
    secret_key = current_app.config["SECRET_KEY"]
    payment = Payment.query.get(request.args["payment_id"])
    # RUB currency code = 643
    # this page for pay in RUB
    code_currency = 643
    payway= "advcash_rub"

    text = (
        ":".join([
            str(payment.sum),
            str(code_currency),
            payway,
            str(shop_id),
            str(payment.id),
        ])
    ) + secret_key
    SignatureValue = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()  # amount:currency:payway:shop_id:shop_order_idsecret_key

    pay_request = requests.post(
        'https://core.piastrix.com/invoice/create',
        json={
            "description": payment.product_description,
            "amount": payment.sum,
            "currency": code_currency,
            "payway": payway,
            "shop_id": shop_id,
            "shop_order_id": payment.id,
            "sign": SignatureValue,
        }
    )

    dict_response = pay_request.json()
    if not dict_response["data"]:
        db.session.delete(payment)
        db.session.commit()
        flash(f"Error: {dict_response['message']}")

    return render_template('invoice.html', data=dict_response["data"])
