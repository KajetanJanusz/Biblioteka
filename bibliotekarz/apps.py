from django.apps import AppConfig


class BibliotekarzConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'bibliotekarz'

    def ready(self) -> None:
        import bibliotekarz.signals