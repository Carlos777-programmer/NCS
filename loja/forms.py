from django import forms
from .models import ProdutoLoja

class ProdutoLojaForm(forms.ModelForm):
    class Meta:
        model = ProdutoLoja
        fields = [
            'name', 
            'ritual', 
            'icon', 
            'tag', 
            'rank', 
            'description', 
            'price', 
            'volume', 
            'rendimento', 
            'ph', 
            'durabilidade', 
            'affiliate_url', 
            'verified_partner', 
            'image'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ritual': forms.Select(attrs={'class': 'form-control'}),
            'icon': forms.TextInput(attrs={'class': 'form-control'}),
            'tag': forms.TextInput(attrs={'class': 'form-control'}),
            'rank': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'volume': forms.TextInput(attrs={'class': 'form-control'}),
            'rendimento': forms.TextInput(attrs={'class': 'form-control'}),
            'ph': forms.TextInput(attrs={'class': 'form-control'}),
            'durabilidade': forms.TextInput(attrs={'class': 'form-control'}),
            'affiliate_url': forms.URLInput(attrs={'class': 'form-control'}),
        }