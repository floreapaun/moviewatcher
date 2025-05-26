from django.apps import AppConfig

class MyAppConfig(AppConfig):
    name = "movies"

    def ready(self):
        import movies.signals

