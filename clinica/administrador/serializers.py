from clinicaEstetica.serializer import UserSerializer
from rest_framework import serializers

from django.contrib.auth.models import User
from .models import Administrador
from profissional.models import Profissional
from servico.models import Servico, TipoServico
from cliente.models import Cliente
from plano.models import Plano

# class AdministradorSerializer(serializers.ModelSerializer):
#     user = User
#     class Meta:
#         model = Administrador
#         fields = "__all__"

class AdministradorSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # aceita dados aninhados

    class Meta:
        model = Administrador
        fields = "__all__"  # ou "__all__" se preferir

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        administrador = Administrador.objects.create(
            user=user,
            nome=validated_data.get('nome', '')
        )
        return administrador
    
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