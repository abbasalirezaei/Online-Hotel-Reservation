from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Hotel Reservation API",
      default_version='v1',
      description="API documentation for the hotel booking system",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="your-email@example.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('hotel/', include('apps.hotel.urls')),
    path('reservations/', include('apps.reservations.urls', namespace='reservations')),
    path('reviews/', include('apps.reviews.urls')),
    path('notifications/', include('apps.notifications.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]





# swagger and redoc URLs
urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
