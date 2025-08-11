from django.apps import AppConfig

# import importlib
    # name = 'apps.accounts'

    # def ready(self):
        # importlib.import_module('apps.accounts.signals')
class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    def ready(self):
        import apps.accounts.signals