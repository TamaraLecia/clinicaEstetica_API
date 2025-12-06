from rest_framework import serializers
from servico.models import Servico, TipoServico, Agendamento
from profissional.models import Profissional
from django.contrib.auth.models import User

class ServicoSerializer(serializers.ModelSerializer):
    # Campos extras que não exitem no modelo, mas que eu preciso para adicionar o serviço
    # tipo__nome é categoria
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
    
    # função serializer de atualizar profissional
    def update(self, instance, validated_data):
        # instance é objeto do modelo que vai ser atualizado
        # validated_data é os dados validados vindos da requisição
        # Atualiza o tipo de categoria do serviço
        tipo_nome = validated_data.pop("tipo_nome", None)

        if tipo_nome:
            try:
                tipo_objeto = TipoServico.objects.get(categoria=tipo_nome)
                instance.tipo = tipo_objeto
            except TipoServico.DoesNotExist:
                raise serializers.ValidationError({"tipo_nome": "Tipo de serviço não encontrado"})
        
        # Atualiza o profissional que está fazendo o serviço
        profissional_nome = validated_data.pop("profissional_nome", None)
        
        if profissional_nome:
            try:
                profissional_objeto = Profissional.objects.get(nome = profissional_nome)
                instance.profissional = profissional_objeto
            except Profissional.DoesNotExist:
                raise serializers.ValidationError({"profissional_nome": "Profissional não encontrado"})
            
        # Atializando as outras informações do serviço
        for attr, value in validated_data.items():
            # O setattr atualiza cada atributo da instancia com o valor correspondente
            setattr(instance, attr, value)
        # Salva as alterações no banco de dados
        instance.save()
        # retorna o modelo atualizado para o django Rest framework
        return instance



class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServico
        fields = "__all__"


class AgendamentoSerializer(serializers.ModelSerializer):
    servico_nome = serializers.CharField(write_only=True, required=True)
    profissional_nome = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Agendamento
        fields = [
            "id",
            "data",
            "observacoes",
            "servico_nome",
            "profissional_nome",
            "cliente",
            "servico",
            "profissional"
        ]
        read_only_fields = ["cliente", "servico", "profissional"]

    def validate(self, data):
        profissional = data.get("profissional")
        data_agendamento = data.get("data")

        if profissional and data_agendamento:
            conflito = Agendamento.objects.filter(
                profissional=profissional,
                data=data_agendamento
            ).exists()
            if conflito:
                raise serializers.ValidationError(
                    {"detail": "Este profissional já possui um agendamento neste horário"}
                )
        return data

    def create(self, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            raise serializers.ValidationError({"detail": "Usuário não autenticado"})

        validated_data["cliente"] = request.user  

        servico_nome = validated_data.pop("servico_nome", None)
        profissional_nome = validated_data.pop("profissional_nome", None)

        if servico_nome:
            try:
                servico = Servico.objects.get(servico=servico_nome)  # campo correto
                validated_data["servico"] = servico
            except Servico.DoesNotExist:
                raise serializers.ValidationError({"servico_nome": "Serviço não encontrado"})

        if profissional_nome:
            try:
                profissional = Profissional.objects.get(nome=profissional_nome)
                validated_data["profissional"] = profissional
            except Profissional.DoesNotExist:
                raise serializers.ValidationError({"profissional_nome": "Profissional não encontrado"})

        return Agendamento.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.data = validated_data.get("data", instance.data)
        instance.observacoes = validated_data.get("observacoes", instance.observacoes)

        servico_nome = validated_data.pop("servico_nome", None)
        profissional_nome = validated_data.pop("profissional_nome", None)

        if servico_nome:
            try:
                instance.servico = Servico.objects.get(servico=servico_nome)  # campo correto
            except Servico.DoesNotExist:
                raise serializers.ValidationError({"servico_nome": "Serviço não encontrado"})

        if profissional_nome:
            try:
                instance.profissional = Profissional.objects.get(nome=profissional_nome)
            except Profissional.DoesNotExist:
                raise serializers.ValidationError({"profissional_nome": "Profissional não encontrado"})

        instance.save()
        return instance

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["servico"] = instance.servico.servico  # campo correto
        rep["profissional"] = instance.profissional.nome
        rep["cliente"] = instance.cliente.username
        return rep
