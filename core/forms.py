from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import Cliente, Veiculo

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