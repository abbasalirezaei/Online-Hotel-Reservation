import uuid
import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user_factory(db):
    def create_user(**kwargs):
        suffix = uuid.uuid4().hex[:6]  
        defaults = {
            "email": kwargs.get("email", f"user{suffix}@example.com"),
            "phone_number": kwargs.get("phone_number", f"0912{suffix}"),
            "password": kwargs.get("password", "SuperSecure123!"),
            "is_active": True,
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    return create_user