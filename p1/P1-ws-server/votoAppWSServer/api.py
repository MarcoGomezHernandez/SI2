from rest_framework import viewsets
from .models import Censo, Voto
from .serializers import CensoSerializer, VotoSerializer

class CensoViewSet(viewsets.ModelViewSet):
    queryset = Censo.objects.all()
    serializer_class = CensoSerializer

class VotoViewSet(viewsets.ModelViewSet):
    queryset = Voto.objects.all()
    serializer_class = VotoSerializer
