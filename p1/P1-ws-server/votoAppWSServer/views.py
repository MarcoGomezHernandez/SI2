from django.forms.models import model_to_dict
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Censo, Voto
from .serializers import VotoSerializer
from .votoDB import registrar_voto, eliminar_voto, verificar_censo

@api_view(['POST'])
def aportarinfo_censo(request):
    """
    Endpoint para validar la existencia del votante en el censo.
    Recibe la información del votante en el request.data.
    Devuelve HTTP_200_OK y un mensaje de éxito si el votante existe;
    o HTTP_404_NOT_FOUND si no se encuentra.
    """
    censo_data = request.data
    if verificar_censo(censo_data):
        return Response({'message': 'Votante encontrado en el Censo.'},
                        status=status.HTTP_200_OK)
    return Response({'message': 'Datos no encontrados en Censo.'},
                    status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def aportarinfo_voto(request):
    """
    Endpoint para registrar un voto.
    Recibe en el request.data la información del voto, que debe incluir
    el identificador de censo (numeroDNI o censo) del votante.
    Devuelve:
      - HTTP_200_OK y el voto registrado tras serialización si todo es correcto,
      - HTTP_404_NOT_FOUND si el votante no se encuentra en el censo,
      - HTTP_400_BAD_REQUEST en el resto de los casos.
    """
    voto_data = request.data
    numero_dni = voto_data.get('censo', None)
    if not numero_dni:
        return Response({'message': 'Identificador de censo no proporcionado.'},
                        status=status.HTTP_400_BAD_REQUEST)
    if not Censo.objects.filter(numeroDNI=numero_dni).exists():
        return Response({'message': 'Votante no existe en el Censo.'},
                        status=status.HTTP_404_NOT_FOUND)
    voto = registrar_voto(voto_data)
    if voto is None:
        return Response({'message': 'Error registrando voto.'},
                        status=status.HTTP_400_BAD_REQUEST)
    return Response(model_to_dict(voto), status=status.HTTP_200_OK)

@api_view(['GET'])
def getvotos(request):
    """
    Endpoint para consultar los votos de un proceso electoral.
    Se debe enviar el identificador del proceso electoral como parámetro
    'idProcesoElectoral' en la query string.
    Devuelve:
      - HTTP_200_OK y el listado de votos (serializados) si se encuentran registros,
      - HTTP_404_NOT_FOUND si no hay votos asociados.
    """
    id_proceso = request.GET.get('idProcesoElectoral', None)
    if not id_proceso:
        return Response({'message': 'idProcesoElectoral no proporcionado.'},
                        status=status.HTTP_400_BAD_REQUEST)
    votos = Voto.objects.filter(idProcesoElectoral=id_proceso)
    if not votos.exists():
        return Response({'message': 'No existen votos para este proceso electoral.'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = VotoSerializer(votos, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delvoto(request):
    """
    Endpoint para eliminar un voto.
    Se debe enviar el identificador del voto como parámetro 'idVoto'
    en la query string.
    Devuelve:
      - HTTP_200_OK y un mensaje de éxito si se elimina el voto,
      - HTTP_404_NOT_FOUND si no existe el voto.
    """
    id_voto = request.GET.get('idVoto', None)
    if not id_voto:
        return Response({'message': 'idVoto no proporcionado.'},
                        status=status.HTTP_400_BAD_REQUEST)
    if not Voto.objects.filter(pk=id_voto).exists():
        return Response({'message': 'El voto no existe.'},
                        status=status.HTTP_404_NOT_FOUND)
    eliminar_voto(id_voto)
    return Response({'message': 'Voto eliminado correctamente.'},
                    status=status.HTTP_200_OK)