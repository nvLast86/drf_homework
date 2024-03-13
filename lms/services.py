import stripe

from config import settings
from lms.models import Course
from users.models import User

stripe.api_key = settings.STRIPE_API_KEY


def stripe_create_session(course: Course, user: User):
    """Создает сессию"""
    session = stripe.checkout.Session.create(
        success_url='https://example.com/success',
        line_items=[
            {
                'price_data': course.stripe_price_data,
                'quantity': 1,
            }
        ],
        mode='payment',
        customer_email=user.email,
        # cancel_url='https://example.com/cancel'
    )
    return session


def stripe_retrieve_session(stripe_id) -> dict:
    """Возвращает информацию по сессии"""
    return stripe.checkout.Session.retrieve(stripe_id)
