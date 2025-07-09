from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('hotel/', include('hotel.urls')),
    path('reservations/', include('reservations.urls')),
    path('reviews/', include('reviews.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
