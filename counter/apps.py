from django.apps import AppConfig


class CounterConfig(AppConfig):
    name = 'counter'

    def ready(self) :
        from jobs import updater
        updater.start()