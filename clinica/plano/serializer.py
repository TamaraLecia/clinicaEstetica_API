from servico.models import Servico
from rest_framework import serializers
from plano.models import Plano

class PlanoSerializer(serializers.ModelSerializer):
    # Campos extras que não exitem no modelo, mas que eu preciso para adicionar o serviço
    # tipo__nome é categoria
    servico_nome = serializers.CharField(write_only=True)

    # Campos de leitura para mostrar os nomes no GET
    servico = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Plano
        fields = ["id", "tipo", "preco","servico", "servico_nome"]

    def create(self, validated_data):
        # Pega os nomes enviados no JSON
        servico_nome = validated_data.pop("servico_nome")

        # Busca o nome do serviço no banco de dados
        tipo_objeto = Servico.objects.get(servico=servico_nome)
        # criar o plano associado com os serviços

        plano = Plano.objects.create(**validated_data)
        plano.servico.set([tipo_objeto])
        return plano
            
    
    # função serializer de atualizar profissional
    def update(self, instance, validated_data):
        # instance é objeto do modelo que vai ser atualizado
        # validated_data é os dados validados vindos da requisição
        # Atualiza o tipo de categoria do serviço
        servico_nome = validated_data.pop("servico_nome", None)

        if servico_nome:
            try:
                tipo_objeto = Plano.objects.get(servico=servico_nome)
                instance.tipo = tipo_objeto
            except Plano.DoesNotExist:
                raise serializers.ValidationError({"servico_nome": "Serviço não encontrado"})
        
        # Atualizando as outras informações do serviço
        for attr, value in validated_data.items():
            # O setattr atualiza cada atributo da instancia com o valor correspondente
            setattr(instance, attr, value)
        # Salva as alterações no banco de dados
        instance.save()
        # retorna o modelo atualizado para o django Rest framework
        return instance
