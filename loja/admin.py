from django.contrib import admin
from .models import ProdutoLoja

@admin.register(ProdutoLoja)
class ProdutoLojaAdmin(admin.ModelAdmin):
    list_display = ('name', 'ritual', 'price', 'verified_partner', 'rank')
    list_filter = ('ritual', 'verified_partner')
    search_fields = ('name', 'description', 'tag')
    list_editable = ('price', 'verified_partner', 'rank')