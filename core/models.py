from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome

class Veiculo(models.Model):
    cliente = models.ForeignKey(Cliente, related_name='veiculos', on_delete=models.CASCADE)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    placa = models.CharField(max_length=10, unique=True)
    ano = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.modelo} - {self.placa}"

class Servico(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    custo_estimado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Custo de produtos gastos no serviço")

    def __str__(self):
        return f"{self.nome} - R$ {self.preco}"

class OrdemServico(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('EM_ANDAMENTO', 'Em Andamento'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    servicos = models.ManyToManyField(Servico)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    observacoes = models.TextField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OS #{self.id} - {self.cliente.nome} ({self.veiculo.placa})"