from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('apps.accounts.urls')),
    path('hotel/', include('apps.hotel.urls')),
    path('reservations/', include('apps.reservations.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('notifications/', include('apps.notifications.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]