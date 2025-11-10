# /config/celery.py

import os
from celery import Celery

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Cria a instância da aplicação Celery
# O nome 'config' deve bater com o nome do projeto
app = Celery('config')

# Carrega as configurações do Django para o Celery, usando o prefixo 'CELERY_'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre as tasks automaticamente em todos os apps instalados
# (Ele vai procurar por um arquivo 'tasks.py' em cada app)
app.autodiscover_tasks()