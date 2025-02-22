from rest_framework import serializers
from .models import Censo, Voto


class CensoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Censo model.

    This serializer excludes the 'anioCenso' field from the serialized
    representation.

    Attributes:
        Meta (class): Meta options for the CensoSerializer.
            model (Censo): The model that is being serialized.
            exclude (list): List of fields to exclude from the serialized
            representation.
    """
    class Meta:
        model = Censo
        exclude = ['anioCenso']


class VotoSerializer(serializers.ModelSerializer):
    """
    Serializer for the Voto model.

    This serializer includes all fields from the Voto model in the serialized
    representation.

    Attributes:
        Meta (class): Meta options for the VotoSerializer.
            model (Voto): The model that is being serialized.
            fields (str): String indicating that all fields should be included
            in the serialized representation.
    """
    class Meta:
        model = Voto
        fields = "__all__"
