from django.urls import path
from . import views
from .views import ProdutoLojaListAPIView, novo_produto_ia_view, api_extrair_produto_ia, vitrine_loja_view

urlpatterns = [
    path('', vitrine_loja_view, name='loja_vitrine'),
    path('api/produtos/', ProdutoLojaListAPIView.as_view(), name='api_produtos_list'),
    path('gerenciar/novo-ia/', novo_produto_ia_view, name='novo_produto_ia'),
    path('api/extrair-ia/', api_extrair_produto_ia, name='api_extrair_ia'),
    path('gerenciar/', views.gerenciar_produtos, name='gerenciar_produtos'),
    path('editar/<int:pk>/', views.editar_produto, name='editar_produto'),
    path('excluir/<int:pk>/', views.excluir_produto, name='excluir_produto'),
]