from django.db import models
from django.contrib.auth.models import User

class AuditLog(models.Model):
    """
    Cumpre o item 3.1.i (Auditabilidade) do Edital.
    Registra todas as interações do usuário com a IA.
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    prompt = models.TextField(verbose_name="Prompt do Usuário")
    response = models.TextField(verbose_name="Resposta da IA")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data e Hora")

    def __str__(self):
        return f'Log de {self.user.username or "Anônimo"} em {self.created_at.strftime("%Y-%m-%d %H:%M")}'

    class Meta:
        verbose_name = "Log de Auditoria"
        verbose_name_plural = "Logs de Auditoria"
        ordering = ['-created_at']