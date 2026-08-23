from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    CustomLoginView, dashboard, 
    clientes_list, cliente_create, 
    veiculos_list, veiculo_create,
    agendamento_create, agendamentos_list,
)

urlpatterns = [
    path('', CustomLoginView.as_main_view() if hasattr(CustomLoginView, 'as_main_view') else CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientes/', clientes_list, name='clientes_list'),
    path('clientes/novo/', cliente_create, name='cliente_create'),
    path('veiculos/', veiculos_list, name='veiculos_list'),
    path('veiculos/novo/', veiculo_create, name='veiculo_create'),
    path('ordens-servico/', views.ordens_servico_list, name='ordens_servico_list'),
    path('ordens-servico/novo/', views.ordem_servico_create, name='ordem_servico_create'),
    path('ordens/<int:pk>/editar/', views.OrdemServicoUpdateView.as_view(), name='ordem_servico_update'),
    path('ordens/<int:pk>/excluir/', views.OrdemServicoDeleteView.as_view(), name='ordem_servico_delete'),
    path('servicos/', views.ServicoListView.as_view(), name='servicos_list'),
    path('servicos/novo/', views.ServicoCreateView.as_view(), name='servico_create'),
    path('servicos/<int:pk>/editar/', views.ServicoUpdateView.as_view(), name='servico_update'),
    path('servicos/<int:pk>/excluir/', views.ServicoDeleteView.as_view(), name='servico_delete'),
    path('agendamentos/', agendamentos_list, name='agendamentos_list'),
    path('agendamentos/novo/', agendamento_create, name='agendamento_create'),
    path('gastos/', views.gastos_list, name='gastos_list'),
    path('gastos/novo/', views.gasto_create, name='gasto_create'),
    path('gastos/deletar/<int:pk>/', views.gasto_delete, name='gasto_delete'),
]