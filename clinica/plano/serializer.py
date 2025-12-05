from rest_framework import serializers
from plano.models import Plano
from django.contrib.auth.models import User

class PlanoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plano
        fields = '_all_'

    # Função para criar um plano
    def create(self, validated_data):
        plano = Plano.objects.create(**validated_data)
        return plano

    # Função para editar/atualizar um plano
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance