from servico.models import Servico
from rest_framework import serializers
from plano.models import Plano

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ["id", "servico"]

class PlanoSerializer(serializers.ModelSerializer):
    # Serializa os serviços como lista de objetos
    servico = ServicoSerializer(many=True, read_only=True)

    # Para criar/atualizar,
    servico_ids = serializers.PrimaryKeyRelatedField(
        queryset=Servico.objects.all(),
        many=True,
        write_only=True,
        required =False
    )

    class Meta:
        model = Plano
        fields = ["id", "tipo", "preco", "servico", "servico_ids"]

    def create(self, validated_data):
        servicos = validated_data.pop("servico_ids", [])
        plano = Plano.objects.create(**validated_data)
        plano.servico.set(servicos)
        return plano

    def update(self, instance, validated_data):
        servicos = validated_data.pop("servico_ids", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if servicos is not None:
            instance.servico.set(servicos)
        return instance