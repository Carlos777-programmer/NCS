from django.db import models

class ProdutoLoja(models.Model):
    RITUAL_CHOICES = [
        ('lavagem', 'Lavagem'),
        ('blindagem', 'Blindagem'),
        ('acabamento', 'Acabamento'),
    ]

    name = models.CharField(max_length=150, verbose_name="Nome do Produto")
    ritual = models.CharField(max_length=50, choices=RITUAL_CHOICES, default='lavagem', verbose_name="Etapa / Ritual")
    icon = models.CharField(max_length=50, default='droplets', verbose_name="Ícone (Lucide)")
    tag = models.CharField(max_length=100, verbose_name="Tag / Destaque")
    rank = models.IntegerField(default=1, verbose_name="Ordem de Exibição")
    description = models.TextField(verbose_name="Descrição")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Preço (R$)")
    
    # Especificações técnicas
    volume = models.CharField(max_length=50, default='A confirmar', verbose_name="Volume")
    rendimento = models.CharField(max_length=50, default='A confirmar', verbose_name="Rendimento")
    ph = models.CharField(max_length=50, default='A confirmar', verbose_name="pH")
    durabilidade = models.CharField(max_length=50, default='A confirmar', verbose_name="Durabilidade")

    # Links e imagens
    image = models.ImageField(upload_to='produtos/', null=True, blank=True, verbose_name="Foto do Produto")
    affiliate_url = models.URLField(max_length=500, blank=True, verbose_name="Link de Afiliado / Compra")
    verified_partner = models.BooleanField(default=False, verbose_name="Parceiro Verificado / Ativo")

    class Meta:
        verbose_name = "Produto da Loja"
        verbose_name_plural = "Produtos da Loja"
        ordering = ['rank']

    def __str__(self):
        return self.name