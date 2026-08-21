import json
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.serializers.json import DjangoJSONEncoder
from .models import Cliente, Veiculo, OrdemServico, Servico, Agendamento
from .forms import ClienteForm, VeiculoForm, LoginForm, OrdemServicoForm, ServicoForm, AgendamentoForm

def login_view(request):
    return render(request, 'core/login.html')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    mes_atual = hoje.month
    ano_atual = hoje.year

    # 1. Contadores para os Cards
    em_execucao = OrdemServico.objects.filter(status='EM ANDAMENTO').count()
    
    concluidos_hoje = OrdemServico.objects.filter(
        status='CONCLUIDO', 
        criado_em__date=hoje
    ).count()

    # 2. Faturamento do mês atual (somando o valor das OS concluídas no mês)
    faturamento_mensal = OrdemServico.objects.filter(
        status='CONCLUIDO',
        criado_em__month=mes_atual,
        criado_em__year=ano_atual
    ).aggregate(total=Sum('valor_total'))['total'] or 0

    # 3. Ordens de Serviço Recentes (últimas 5)
    recentes_os = OrdemServico.objects.all().order_by('-criado_em')[:5]

    context = {
        'em_execucao': em_execucao,
        'concluidos_hoje': concluidos_hoje,
        'faturamento_mensal': faturamento_mensal,
        'recentes_os': recentes_os,
    }
    return render(request, 'core/dashboard.html', context)

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
    servicos_precos = list(Servico.objects.values('id', 'preco'))
    servicos_json = json.dumps(servicos_precos, cls=DjangoJSONEncoder)

    return render(
        request,
        'core/ordem_servico_form.html',
        {'form': form, 'servicos_json': servicos_json},
    )

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

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    servicos_precos = list(Servico.objects.values('id', 'preco'))
    context['servicos_json'] = json.dumps(
        servicos_precos, cls=DjangoJSONEncoder
    )
    return context

class OrdemServicoDeleteView(DeleteView):
    model = OrdemServico
    template_name = 'core/ordem_servico_confirm_delete.html'
    success_url = reverse_lazy('ordens_servico_list')

def agendamentos_list(view_func):
    agendamentos = Agendamento.objects.all().order_by('data_hora')
    return render(view_func, 'core/agendamento_list.html', {'agendamentos': agendamentos})

def agendamento_create(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendamentos_list')
    else:
        form = AgendamentoForm()
    return render(request, 'core/agendamento_form.html', {'form': form})