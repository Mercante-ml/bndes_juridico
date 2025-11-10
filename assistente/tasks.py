import os
import google.generativeai as genai
from celery import shared_task
from django.contrib.auth.models import User
from .models import AuditLog

# Configura a API do Gemini usando a chave do seu .env
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada no .env")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')


@shared_task
def processar_chat_gemini_task(prompt_texto, user_id):
    """
    Task assíncrona que chama a IA e cumpre o Edital:
    1. Chama a ferramenta de IA (Item 1.1)
    2. Salva na base auditável (Item 3.1.i)
    """
    try:
        # 1. Chama a IA (Edital Item 1.1)
        # O prompt é simples, mas cumpre o "propor manifestação" (Item 2.5.b)
        # Estamos "fingindo" que o prompt é um pedido jurídico.
        prompt_completo = f"""
        Você é um assistente jurídico. Responda a seguinte solicitação:
        "{prompt_texto}"
        """
        response = model.generate_content(prompt_completo)
        response_text = response.text

    except Exception as e:
        response_text = f"Erro ao processar a solicitação de IA: {str(e)}"

    try:
        # 2. Salva na Base Auditável (Edital Item 3.1.i)
        user = User.objects.get(id=user_id) if user_id else None
        AuditLog.objects.create(
            user=user,
            prompt=prompt_texto,
            response=response_text
        )
    except Exception as e:
        # Se a auditoria falhar, pelo menos retorne a resposta
        print(f"Erro ao salvar no AuditLog: {str(e)}")

    return response_text