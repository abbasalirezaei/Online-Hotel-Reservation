import pytest
from unittest.mock import patch
from django.core import mail
from apps.accounts.tasks import send_activation_email_task
from django.utils import timezone
from apps.accounts.models import User


@patch("apps.accounts.tasks.render_to_string", return_value="<p>Mocked HTML</p>")
@pytest.mark.django_db
def test_send_activation_email_success(mock_render, customer_user):
    result = send_activation_email_task(customer_user.id, customer_user.email)

    customer_user.refresh_from_db()
    assert result is True
    assert customer_user.active_code is not None
    assert customer_user.active_code_expires_at > timezone.now()
    assert len(mail.outbox) == 1
    assert customer_user.email in mail.outbox[0].to


@pytest.mark.django_db
def test_send_activation_email_user_not_found():
    result = send_activation_email_task(9999, "ghost@example.com")
    assert result is False


@patch(
    "apps.accounts.tasks.EmailMultiAlternatives.send",
    side_effect=Exception("SMTP error"),
)
@pytest.mark.django_db
def test_send_activation_email_send_failure(mock_send, customer_user):
    result = send_activation_email_task(customer_user.id, customer_user.email)
    assert result is False
