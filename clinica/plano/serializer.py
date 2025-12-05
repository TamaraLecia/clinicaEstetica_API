from rest_framework import serializers
from plano.models import Plano
from django.contrib.auth.models import User

class PlanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plano
        fields = '__all__'
