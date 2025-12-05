from rest_framework import serializers
from .models import Cliente
from clinicaEstetica.serializer import UserSerializer
from django.contrib.auth.models import User


class ClienteSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # aceita dados aninhados

    class Meta:
        model = Cliente
        fields = "__all__"  # ou "__all__" se preferir

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        cliente = Cliente.objects.create(
            user=user,
            nome=validated_data.get('nome', ''),
            cpf=validated_data.get('cpf', ''),
            endereco=validated_data.get('endereco', ''),
            telefone=validated_data.get('telefone', ''),
        )
        return cliente
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            instance.user.username = user_data.get('username', instance.user.username)
            instance.user.email=user_data.get('email', instance.user.email)

            instance.user.save()
        
        instance.nome=validated_data.get('nome', instance.nome)
        instance.cpf=validated_data.get('cpf', instance.cpf)
        instance.endereco=validated_data.get('endereco', instance.endereco)
        instance.telefone=validated_data.get('telefone', instance.telefone)
        
        instance.save()
        return instance


# foi utilizado o serializers.Serializer por que não estou alterando ou criando um modelo diretamente
class AlterarSenhaSerializer(serializers.Serializer):
    username = serializers.CharField()
    senha = serializers.CharField()
    senhaConfirme = serializers.CharField()

    def validate(self, data):
        if data['senha'] != data['senhaConfirme']:
            raise serializers.ValidationError({"Senha incorreta"})
        return data

    def save(self):
        username = self.validated_data['username']
        senha = self.validated_data['senha']
        usuario = User.objects.get(username=username)
        usuario.set_password(senha)
        usuario.save()
        return usuario



















# class ClienteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cliente
#         fields = "__all__"

# class AlterarSenhaSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     senha = serializers.CharField(write_only=True)
    
#     def save(self):
#         username = self._validated_data['username']
#         senha = self.validated_data['senha']
#         usuario = User.objects.get(username=username)
#         usuario.set_password(senha)
#         usuario.save()
#         return usuario