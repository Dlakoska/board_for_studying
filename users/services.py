import stripe
from forex_python.converter import CurrencyRates

from config.settings import STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY


def convert_currency(amount):
    c = CurrencyRates()
    rate = c.get_rate('RUB', 'USD')
    return int(amount * rate)


def create_stripe_product(prod):
    """ Создание продукта в страйпе """
    stripe_product = stripe.Product.create(name=prod)
    return stripe_product


def create_stripe_price(amount, product_id):
    """ Создание цены в страйпе """
    return stripe.Price.create(
        currency="rub",
        unit_amount=int(amount * 100),
        product_data={"name": product_id},
    )


def create_stripe_session(price):
    """ Создание сессии на оплату в страйпе """
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/", # куда перенаправляется пользователь после успешной оплаты
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )
    return session.id, session.url
