from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Cliente, Veiculo, OrdemServico, Servico
from .forms import ClienteForm, VeiculoForm, LoginForm, OrdemServicoForm, ServicoForm

def login_view(request):
    return render(request, 'core/login.html')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    return render(request, 'core/dashboard.html')

@login_required
def clientes_list(request):
    clientes = Cliente.objects.all().order_by('-criado_em')
    return render(request, 'core/clientes_list.html', {'clientes': clientes})

@login_required
def cliente_create(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm()
    return render(request, 'core/cliente_form.html', {'form': form})

@login_required
def veiculos_list(request):
    veiculos = Veiculo.objects.all().select_related('cliente').order_by('-id')
    return render(request, 'core/veiculos_list.html', {'veiculos': veiculos})

@login_required
def veiculo_create(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('veiculos_list')
    else:
        form = VeiculoForm()
    return render(request, 'core/veiculo_form.html', {'form': form})

@login_required
def ordens_servico_list(request):
    ordens = OrdemServico.objects.all().order_by('-criado_em')
    return render(request, 'core/ordens_servico_list.html', {'ordens': ordens})

@login_required
def ordem_servico_create(request):
    if request.method == 'POST':
        form = OrdemServicoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('ordens_servico_list')
    else:
        form = OrdemServicoForm()
    return render(request, 'core/ordem_servico_form.html', {'form': form})

class ServicoListView(ListView):
    model = Servico
    template_name = 'core/servico_list.html'

class ServicoCreateView(CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'core/servico_form.html'
    success_url = reverse_lazy('servicos_list')

class ServicoUpdateView(UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'core/servico_form.html'
    success_url = reverse_lazy('servicos_list')

class ServicoDeleteView(DeleteView):
    model = Servico
    template_name = 'core/servico_confirm_delete.html'
    success_url = reverse_lazy('servicos_list')

class OrdemServicoUpdateView(UpdateView):
    model = OrdemServico
    form_class = OrdemServicoForm
    template_name = 'core/ordem_servico_form.html'
    success_url = reverse_lazy('ordens_servico_list')

class OrdemServicoDeleteView(DeleteView):
    model = OrdemServico
    template_name = 'core/ordem_servico_confirm_delete.html'
    success_url = reverse_lazy('ordens_servico_list')