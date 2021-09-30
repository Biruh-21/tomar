from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "tomar.apps.account"

    def ready(self):
        import tomar.apps.account.signals
