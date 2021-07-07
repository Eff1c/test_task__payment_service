from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, FloatField, SubmitField
from wtforms.validators import DataRequired
from ..models import Currency


class PaymentForm(FlaskForm):
    sum = FloatField('Sum', validators=[DataRequired("Please enter sum.")])
    product_description = TextAreaField('Description', validators=[DataRequired("Please enter description.")])
    currency = SelectField('Currency', coerce=int, validators=[DataRequired("Please enter currency.")])
    submit = SubmitField('Pay')

    def __init__(self, *args, **kwargs):
        super(PaymentForm, self).__init__(*args, **kwargs)
        self.currency.choices = [(
            currency.id,
            currency.name,
            )\
            for currency in Currency.query.order_by(Currency.id).all()
        ]
