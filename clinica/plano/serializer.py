from servico.models import Servico
from rest_framework import serializers
from plano.models import Plano

# class PlanoSerializer(serializers.ModelSerializer):
#     # Campos extras que não exitem no modelo, mas que eu preciso para adicionar o serviço
#     # tipo__nome é categoria
#     servico_nome = serializers.CharField(write_only=True)

#     # Campos de leitura para mostrar os nomes no GET
#     servico = serializers.StringRelatedField(read_only=True)

#     class Meta:
#         model = Plano
#         fields = ["id", "tipo", "preco","servico", "servico_nome"]

#     def create(self, validated_data):
#         # Pega os nomes enviados no JSON
#         servico_nome = validated_data.pop("servico_nome")

#         # Busca o nome do serviço no banco de dados
#         tipo_objeto = Servico.objects.get(servico=servico_nome)
#         # criar o plano associado com os serviços

#         plano = Plano.objects.create(**validated_data)
#         plano.servico.set([tipo_objeto])
#         return plano
    
    # plano/serializers.py
from rest_framework import serializers
from plano.models import Plano
from servico.models import Servico


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

    
    