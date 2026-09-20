from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('garage.urls')),    # Rotas da API para o site / simulador
    path('', include('core.urls')),      # Rotas do sistema principal (login, dashboard, etc.)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
