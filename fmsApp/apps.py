from django.apps import AppConfig

class FmsappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'fmsApp'

    def ready(self):
        # Import signals here to register them
        import fmsApp.signals
