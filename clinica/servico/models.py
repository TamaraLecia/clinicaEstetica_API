from django.db import models
from django.contrib.auth.models import User
from profissional.models import Profissional
from cliente.models import Cliente

class TipoServico(models.Model):
    categoria = models.TextField(max_length=100)
    imagem = models.FileField(upload_to="img_servico")

    def __str__(self):
        return f'Categoria do serviço:{self.categoria}'

class Servico(models.Model):
    #related_name: permite acessar todos os serviços na view ou no template
    tipo = models.ForeignKey(TipoServico, on_delete=models.CASCADE, related_name="tiposServicos")
    servico = models.TextField(max_length=100)
    preco = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='preco')       
    profissional = models.ForeignKey('profissional.Profissional', on_delete=models.CASCADE)
    descricao = models.TextField(max_length=200)
    arquivo = models.FileField(upload_to="img")

    def __str__(self):
        return f'{self.servico}'
    

class Agendamento(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="agendamentos")
    servico = models.ForeignKey(Servico, on_delete=models.CASCADE)
    profissional = models.ForeignKey(Profissional, on_delete=models.CASCADE)
    data = models.DateTimeField()

    formaPagamento_escolha = [('dinheiro', 'Dinheiro'), ('pix', 'Pix'), ('cartao', 'Cartão'),]
    forma_pagamento = models.CharField(max_length=20, choices=formaPagamento_escolha, default='dinheiro')

    def __str__(self):
        return f"{self.cliente.nome} - {self.servico.servico} ({self.forma_pagamento})"



