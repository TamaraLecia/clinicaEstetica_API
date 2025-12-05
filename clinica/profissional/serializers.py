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
