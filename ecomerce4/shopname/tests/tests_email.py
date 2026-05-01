import pytest
from unittest.mock import patch
from shopname.views import send_order_email
from .factories import OrderFactory


@pytest.mark.django_db
@patch("shopname.views.send_mail")
def test_email_sent_successfully(mock_send_mail):
    order = OrderFactory(first_name="John", email="watson@gmail.com", total_price=500)

    send_order_email(order)

    mock_send_mail.assert_called_once()

