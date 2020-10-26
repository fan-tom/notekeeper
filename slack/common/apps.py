from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    REVIEW M1ha:
    1. apps.py можно не определять, если он соответствует стандарту
    2. При создании кастомного apps.py, насколько я помню, его надо указывать в __init__.py в default_app_config
      https://docs.djangoproject.com/en/3.0/ref/applications/#configuring-applications
    """
    name = 'common'
