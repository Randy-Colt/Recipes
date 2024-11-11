from django.apps import AppConfig
from django.core.signals import request_finished


class RecipesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recipes'
    verbose_name = 'РЕЦЕПТЫ'

    def ready(self):
        from recipes import signals
        # request_finished.connect(signals.create_converter)
        # request_finished.connect(signals.auto_delete_file_on_change)
        # request_finished.connect(signals.auto_delete_file_on_delete)
