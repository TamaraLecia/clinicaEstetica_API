from rest_framework import serializers
from servico.models import Servico, TipoServico
from django.contrib.auth.models import User

class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = "__all__"

class CategoriaSerializer(serializers.Serializer):
    class meta:
        model = TipoServico
        fields = "__all__"