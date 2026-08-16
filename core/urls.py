from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, dashboard, 
    clientes_list, cliente_create, 
    veiculos_list, veiculo_create
)

urlpatterns = [
    path('', CustomLoginView.as_main_view() if hasattr(CustomLoginView, 'as_main_view') else CustomLoginView.as_view(), name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('clientes/', clientes_list, name='clientes_list'),
    path('clientes/novo/', cliente_create, name='cliente_create'),
    path('veiculos/', veiculos_list, name='veiculos_list'),
    path('veiculos/novo/', veiculo_create, name='veiculo_create'),
]