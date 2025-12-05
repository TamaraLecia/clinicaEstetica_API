from rest_framework import serializers
from .models import Cliente

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = "__all__"

class AlterarSenhaSerializer(serializers.Serializer):
    username = serializers.CharField()
    senha = serializers.CharField(write_only=True)
    
    def save(self):
        username = self._validated_data['username']
        senha = self.validated_data['senha']
        usuario = User.objects.get(username=username)
        usuario.set_password(senha)
        usuario.save()
        return usuario