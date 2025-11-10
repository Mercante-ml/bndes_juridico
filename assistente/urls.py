from django.urls import path
from .views import ChatApiView, TaskResultView

urlpatterns = [
    # 1. Endpoint para iniciar o chat
    path('api/v1/chat/', ChatApiView.as_view(), name='chat-api'),
    
    # 2. Endpoint para verificar o resultado da tarefa
    path('api/v1/task-result/<str:task_id>/', TaskResultView.as_view(), name='task-result-api'),
]