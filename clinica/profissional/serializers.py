from clinicaEstetica.serializer import UserSerializer
from rest_framework import serializers

from django.contrib.auth.models import User
from profissional.models import Profissional

class ProfissionalSerializer(serializers.ModelSerializer):
    user = UserSerializer()  #faz com que o user aceite os dados aninhados, ou seja, tudo junto

    class Meta:
        model = Profissional
        fields = "__all__"

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            email=user_data['email'],
            password=user_data['password']
        )
        profissional = Profissional.objects.create(
            # Campos obrigatórios
            user=user,
            nome=validated_data.get('nome', ''),
            endereco=validated_data.get('endereco', ''),
            especializacao=validated_data.get('especializacao', ''),
            numTelefone=validated_data.get('numTelefone'),  
            salario=validated_data.get('salario', 0),
            identificador=validated_data.get('identificador', 'profissional')
        )
        return profissional
    
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        if user_data:
            user = instance.user
            user.username = user_data.get('username', user.username)
            user.email = user_data.get('email', user.email)
            user.save()

        instance.nome = validated_data.get('nome', instance.nome)
        instance.numTelefone = validated_data.get('numTelefone', instance)
        instance.endereco = validated_data.get('endereco', instance)
        instance.save()
        return instance

    
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
