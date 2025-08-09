from django.apps import AppConfig


class HotelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hotel'
    verbose_name = "hotel"
    verbose_name_plural = "Hotels"
    
    def ready(self):
        import hotel.signals  