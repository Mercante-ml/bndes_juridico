# /config/__init__.py

# Importa o app Celery que acabamos de criar
from .celery import app as celery_app

# Garante que o app Celery seja carregado
__all__ = ('celery_app',)