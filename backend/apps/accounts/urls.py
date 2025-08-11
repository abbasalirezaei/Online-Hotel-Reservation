from django.urls import path,include

urlpatterns = [
    path("api/v1/", include(("apps.accounts.api.v1.urls", "accounts_v1"), namespace="accounts_v1")),
]   