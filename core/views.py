import json
from django.http import JsonResponse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import timezone
from django.db.models import Sum
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime
from .models import Cliente, Veiculo, OrdemServico, Servico, Agendamento, Gasto
from .forms import ClienteForm, VeiculoForm, LoginForm, OrdemServicoForm, ServicoForm, AgendamentoForm, GastoForm

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
def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('clientes_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/cliente_form.html', {'form': form, 'editando': True})

@login_required
def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('clientes_list')
    return render(request, 'core/cliente_confirm_delete.html', {'cliente': cliente})

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
def veiculo_update(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('veiculos_list')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'core/veiculo_form.html', {'form': form, 'editando': True})

@login_required
def veiculo_delete(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        veiculo.delete()
        return redirect('veiculos_list')
    return render(request, 'core/veiculo_confirm_delete.html', {'veiculo': veiculo})

@login_required
def load_veiculos(request):
    cliente_id = request.GET.get('cliente_id')
    veiculos = Veiculo.objects.filter(cliente_id=cliente_id).values('id', 'marca', 'modelo', 'placa')
    return JsonResponse(list(veiculos), safe=False)

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

class ServicoListView(LoginRequiredMixin, ListView):
    model = Servico
    template_name = 'core/servico_list.html'

class ServicoCreateView(LoginRequiredMixin, CreateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'core/servico_form.html'
    success_url = reverse_lazy('servicos_list')

class ServicoUpdateView(LoginRequiredMixin, UpdateView):
    model = Servico
    form_class = ServicoForm
    template_name = 'core/servico_form.html'
    success_url = reverse_lazy('servicos_list')

class ServicoDeleteView(LoginRequiredMixin, DeleteView):
    model = Servico
    template_name = 'core/servico_confirm_delete.html'
    success_url = reverse_lazy('servicos_list')

class OrdemServicoUpdateView(LoginRequiredMixin, UpdateView):
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

class OrdemServicoDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrdemServico
    template_name = 'core\ordem_servico_confirm_delete.html'  # o caminho do seu template
    success_url = reverse_lazy('ordens_servico_list')

    def test_func(self):
        # Opcional: Garante que apenas usuários específicos ou staff podem excluir
        return self.request.user.is_staff

@login_required
def agendamentos_list(request):
    agendamentos = Agendamento.objects.all().order_by('data_hora')
    return render(request, 'core/agendamento_list.html', {'agendamentos': agendamentos})

@login_required
def agendamento_create(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('agendamentos_list')
    else:
        form = AgendamentoForm()
    return render(request, 'core/agendamento_form.html', {'form': form})

@login_required
def agendamento_update(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            return redirect('agendamentos_list')
    else:
        form = AgendamentoForm(instance=agendamento)
    return render(request, 'core/agendamento_form.html', {'form': form, 'editando': True})

@login_required
def agendamento_delete(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        agendamento.delete()
        return redirect('agendamentos_list')
    return render(request, 'core/agendamento_confirm_delete.html', {'agendamento': agendamento})

@login_required
def gastos_list(request):
    hoje = datetime.today()
    
    tipo_filtro = request.GET.get('tipo', 'mes')
    mes_param = request.GET.get('mes', str(hoje.month).zfill(2))
    trimestre_param = request.GET.get('trimestre', '1')
    semana_param = request.GET.get('semana', str(hoje.isocalendar()[1]))
    ano_param = request.GET.get('ano', str(hoje.year))

    try:
        ano = int(ano_param)
    except ValueError:
        ano = hoje.year

    gastos = Gasto.objects.all().order_by('-data')

    if tipo_filtro == 'mes':
        try:
            mes = int(mes_param)
        except ValueError:
            mes = hoje.month
        gastos = gastos.filter(data__year=ano, data__month=mes)
        
    elif tipo_filtro == 'trimestre':
        try:
            trimestre = int(trimestre_param)
        except ValueError:
            trimestre = 1
        
        meses_map = {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8, 9], 4: [10, 11, 12]}
        meses = meses_map.get(trimestre, [1, 2, 3])
        gastos = gastos.filter(data__year=ano, data__month__in=meses)
        
    elif tipo_filtro == 'semanal':
        try:
            semana = int(semana_param)
        except ValueError:
            semana = hoje.isocalendar()[1]
        gastos = gastos.filter(data__year=ano, data__week=semana)
        
    elif tipo_filtro == 'ano':
        gastos = gastos.filter(data__year=ano)
        
    else:  # 'tudo'
        tipo_filtro = 'tudo'

    total_filtrado = gastos.aggregate(total=Sum('valor'))['total'] or 0
    total_ano = Gasto.objects.filter(data__year=ano).aggregate(total=Sum('valor'))['total'] or 0

    context = {
        'gastos': gastos,
        'total_filtrado': total_filtrado,
        'total_ano': total_ano,
        'tipo_filtro': tipo_filtro,
        'mes_atual': str(mes_param).zfill(2),
        'trimestre_atual': str(trimestre_param),
        'semana_atual': str(semana_param),
        'ano_atual': str(ano),
    }
    return render(request, 'core/gastos_list.html', context)

@login_required
def gasto_create(request):
    if request.method == 'POST':
        form = GastoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('gastos_list')
    else:
        form = GastoForm()
    return render(request, 'core/gasto_form.html', {'form': form})

@login_required
def gasto_delete(request, pk):
    gasto = get_object_or_404(Gasto, pk=pk)
    if request.method == 'POST':
        gasto.delete()
        return redirect('gastos_list')
    return render(request, 'core/gasto_confirm_delete.html', {'gasto': gasto})