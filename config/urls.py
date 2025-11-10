from django.contrib import admin
from django.urls import path, include
# Importações adicionadas
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Nossas URLs da API
    path('', include('assistente.urls')),
    
    # URL principal que serve nosso 'index.html'
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]

# Isso é necessário para o Django servir os arquivos (CSS/JS) da pasta 'static'
# em modo de DESENVOLVIMENTO (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    # Na verdade, para o `STATICFILES_DIRS`, o `static` helper não é necessário
    # A view acima já cuida do index.html. O Django já serve os outros
    # arquivos estáticos automaticamente em DEBUG. Vamos simplificar.