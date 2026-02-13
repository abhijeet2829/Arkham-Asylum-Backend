from django.apps import AppConfig


class ArkhamAppConfig(AppConfig):
    name = 'arkham_app'

    def ready(self):
        import arkham_app.signals