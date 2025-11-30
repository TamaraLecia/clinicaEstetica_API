from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Administrador
from profissional.models import Profissional
from servico.models import Servico, TipoServico
from cliente.models import Cliente
from plano.models import Plano

class AdministradorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Administrador
        fields = "__all__"

class AlterarSenhaSerializer(serializers.ModelSerializer):
    class Meta:
        username = serializers.CharField()
        senha = serializers.CharField()

        def save(self):
            username = self.validated_data['username']
            senha = self.validated_data['senha']
            usuario = User.objects.get(username=username)
            usuario.set_password(senha)
            usuario.save()
            return usuario


class VerProfissionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profissional
        fields = "__all__"

class MostrarServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = "__all__"

class AlterarCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = "__all__"

class VerClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"

class VerPlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = "__all__"