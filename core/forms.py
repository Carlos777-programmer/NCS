from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Cliente, Veiculo, OrdemServico, Servico, Agendamento, Gasto

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Digite seu usuário',
            'class': 'input-custom'
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Digite sua senha',
        })

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'telefone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome completo do cliente'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(00) 00000-0000'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@exemplo.com'}),
        }

class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = ['cliente', 'marca', 'modelo', 'placa', 'ano']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-input'}),
            'marca': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Volkswagen'}),
            'modelo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Gol G5'}),
            'placa': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'ABC-1234 ou ABC1D23', 'style': 'text-transform: uppercase;'}),
            'ano': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '2026'}),
        }

class OrdemServicoForm(forms.ModelForm):
    class Meta:
        model = OrdemServico
        fields = ['cliente', 'veiculo', 'servicos', 'status', 'valor_total', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'servicos': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'valor_total': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Observações...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Começa com o campo de veículos vazio para evitar exibir carros de outros clientes
        self.fields['veiculo'].queryset = Veiculo.objects.none()

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['veiculo'].queryset = Veiculo.objects.filter(cliente_id=cliente_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.cliente:
            self.fields['veiculo'].queryset = Veiculo.objects.filter(cliente=self.instance.cliente)

class ServicoForm(forms.ModelForm):
    class Meta:
        model = Servico
        fields = ['nome', 'descricao', 'preco', 'custo_estimado']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'preco': forms.NumberInput(attrs={'class': 'form-control'}),
            'custo_estimado': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['cliente', 'veiculo', 'data_hora', 'status', 'observacoes']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'veiculo': forms.Select(attrs={'class': 'form-control'}),
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Começa com o campo de veículos vazio
        self.fields['veiculo'].queryset = Veiculo.objects.none()

        if 'cliente' in self.data:
            try:
                cliente_id = int(self.data.get('cliente'))
                self.fields['veiculo'].queryset = Veiculo.objects.filter(cliente_id=cliente_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.cliente:
            self.fields['veiculo'].queryset = Veiculo.objects.filter(cliente=self.instance.cliente)

class GastoForm(forms.ModelForm):
    class Meta:
        model = Gasto
        fields = ['descricao', 'valor', 'data', 'categoria', 'observacoes']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Peças, Água, Luz...'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': '0.00'}),
            'categoria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Operacional, Fixos...'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }   