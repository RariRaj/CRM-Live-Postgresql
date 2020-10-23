from django.apps import AppConfig


class CrmAppConfig(AppConfig):
    name = 'crm_app'

    def ready(self):
        import crm_app.signals
