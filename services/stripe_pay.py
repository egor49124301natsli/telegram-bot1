import os

# Готовые Stripe-ссылки для разных тарифов (берутся из .env)
STRIPE_LINKS = {
    "1day": os.getenv("STRIPE_1DAY"),
    "1month": os.getenv("STRIPE_ONEMONTH"),
    "3month": os.getenv("STRIPE_THREEMONTH"),
    "predict": os.getenv("STRIPE_ONEPREDICT"),
}

def get_stripe_link(tariff: str):
    """
    Возвращает ссылку на оплату Stripe по тарифу.
    tariff — '1day', '1month', '3month', 'predict'
    """
    return STRIPE_LINKS.get(tariff)
