from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profissional(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.TextField(max_length=100)
    endereco = models.CharField(max_length=150)
    especializacao = models.CharField(max_length=100)
    numTelefone =  models.IntegerField()
    salario = models.IntegerField()
    identificador = models.CharField(max_length=20, default='profissional')

    class Meta:
        permissions = (
            ("detail_profissional","Pode ver detalhe do profissional "),
        )

    def __str__(self):
        return f'Profissional: {self.nome} -- Especialização: {self.especializacao}'