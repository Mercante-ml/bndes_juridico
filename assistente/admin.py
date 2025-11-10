from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'prompt', 'created_at')
    list_filter = ('user', 'created_at')
    search_fields = ('prompt', 'response')
    readonly_fields = ('user', 'prompt', 'response', 'created_at')

    def has_add_permission(self, request):
        return False # Ninguém pode criar logs manualmente

    def has_change_permission(self, request, obj=None):
        return False # Ninguém pode alterar logs