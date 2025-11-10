import json # <-- ADICIONE ESTA IMPORTAÇÃO NO TOPO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_celery_results.models import TaskResult
from .tasks import processar_chat_gemini_task

class ChatApiView(APIView):
    """
    Recebe o "prompt conversacional" (Item 2.2 do Edital)
    e inicia a task de IA de forma assíncrona.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        prompt = request.data.get('prompt')
        if not prompt:
            return Response({"error": "Prompt não fornecido."}, status=400)

        task = processar_chat_gemini_task.delay(prompt, request.user.id)
        return Response({"task_id": task.id})


class TaskResultView(APIView):
    """
    Endpoint auxiliar para o frontend perguntar: "A tarefa X já terminou?"
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id, *args, **kwargs):
        try:
            task = TaskResult.objects.get(task_id=task_id)

            if task.status == "SUCCESS":
                
                # --- A CORREÇÃO ESTÁ AQUI ---
                # 'task.result' é uma string JSON (ex: "\"O BNDES \u00e9...\"")
                # 'json.loads' a converte de volta para uma string Python limpa.
                clean_result = json.loads(task.result) 
                
                return Response({
                    "status": "SUCCESS",
                    "result": clean_result # Enviamos a string limpa
                })
                # --- FIM DA CORREÇÃO ---
                
            elif task.status == "FAILURE":
                # Erros também podem vir como JSON
                try:
                    error_result = json.loads(task.result)
                except:
                    error_result = str(task.result)
                return Response({"status": "FAILURE", "result": error_result})
            
            else:
                return Response({"status": task.status})

        except TaskResult.DoesNotExist:
            return Response({"status": "NOT_FOUND"}, status=404)