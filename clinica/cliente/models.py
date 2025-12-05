from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=15, unique=True) #evitar valores duplicados formato 000.000.000-00
    endereco = models.CharField(max_length=100, blank=True)
    telefone = models.IntegerField(max_length=20, blank=True)
    identificador = models.CharField(max_length=20, default='cliente')

    class Meta:
        permissions = (
            ("detail_cliente","Pode ver detalhe do perfil"),
            ("AgendarServico_cliente", "Pode agendar um servico"),
        )
