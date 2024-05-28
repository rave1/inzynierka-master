from django.apps import AppConfig


class WcaConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wca"

    def ready(self) -> None:
        pass
