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
    
# Atualizar dados serializer
class AlterarDadosClienteSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email') # pega o email do usuário logado

    class Meta:
        model = Cliente
        fields = ['nome', 'email']

        def update(self, instance, validated_data):
            # Atualizando o nome do cliente
            instance.nome = validated_data.get('nome', instance.nome)

            # Atualizando o email do cliente
            user_data = validated_data.get('user', {})
            if 'email' in user_data:
                # valida duplicidade de email
                if User.objects.filter(email=user_data['email']).exclude(pk=instance.user.pk).exists():
                    raise serializers.ValidationError({"email": "Este email já está em uso."})
                instance.user.email = user_data['email']
                instance.user.save()
            
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