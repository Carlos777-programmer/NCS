from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('webpush/', include('webpush.urls')),
    path('sw.js', TemplateView.as_view(
        template_name="core/sw.js", 
        content_type="application/javascript"
    ), name='sw.js'),
]