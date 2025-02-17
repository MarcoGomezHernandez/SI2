from rest_framework import serializers
from .models import Censo, Voto

class CensoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Censo
        fields = '__all__'

class VotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voto
        fields = '__all__'
