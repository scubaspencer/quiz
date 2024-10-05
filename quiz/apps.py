from django.apps import AppConfig
from django.utils.module_loading import import_module


class QuizConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "quiz"

    def ready(self):
        # Dynamically import the signals to ensure Profile is created for new users
        import_module("quiz.signals")
