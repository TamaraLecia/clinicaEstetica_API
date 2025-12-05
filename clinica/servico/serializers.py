from rest_framework import serializers
from servico.models import Servico, TipoServico
from profissional.models import Profissional
from django.contrib.auth.models import User

class ServicoSerializer(serializers.ModelSerializer):
    # Campos extras que não exitem no modelo, mas que eu preciso para adicionar o serviço
    tipo_nome = serializers.CharField(write_only=True)
    profissional_nome = serializers.CharField(write_only=True)

    # Campos de leitura para mostrar os nomes no GET
    tipo = serializers.StringRelatedField(read_only=True)
    profissional = serializers.StringRelatedField(read_only=True)


    class Meta:
        model = Servico
        fields = ["id", "servico", "preco", "descricao", "arquivo", "tipo", "profissional", "tipo_nome", "profissional_nome"]

    def create(self, validated_data):
        # Pega os nomes enviados no JSON
        tipo_nome = validated_data.pop("tipo_nome")
        profissional_nome = validated_data.pop("profissional_nome")

        # Busca o nome do tipo de serviço e o nome do profissional no banco de dados
        tipo_objeto = TipoServico.objects.get(categoria=tipo_nome)
        profissional_objeto = Profissional.objects.get(nome=profissional_nome)

        # criar o serviço associado com o tipo do serviço e o nome do profissional
        return Servico.objects.create(
            tipo = tipo_objeto,
            profissional = profissional_objeto,
            **validated_data
        )

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = "__all__"