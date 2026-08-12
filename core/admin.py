from django.contrib import admin
from .models import Cliente, Veiculo, Servico, OrdemServico

admin.site.register(Cliente)
admin.site.register(Veiculo)
admin.site.register(Servico)
admin.site.register(OrdemServico)
