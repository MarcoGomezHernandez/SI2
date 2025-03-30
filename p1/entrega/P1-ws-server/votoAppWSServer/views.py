from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import VotoSerializer
from .models import Censo, Voto
from django.forms.models import model_to_dict
from .votoDB import verificar_censo, eliminar_voto, get_votos_from_db


class CensoView(APIView):
    """
    API endpoint to collect censo information.
    and check if the person is in the censo.
    """

    def post(self, request, format=None):
        data = request.data

        claves_esperadas = {"numeroDNI", "nombre", "fechaNacimiento",
                            "codigoAutorizacion"}

        if set(data.keys()) == claves_esperadas and verificar_censo(data):
            return Response({'message': 'Datos encontrados en Censo.'},
                            status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Datos no encontrados en Censo.'},
                            status=status.HTTP_404_NOT_FOUND)


class VotoView(APIView):
    """
    API endpoint to collect voto information.
    and save it in the database.
    """

    def post(self, request, format=None):
        data = request.data
        censo_id = data.get('censo_id')

        try:
            censo = Censo.objects.get(pk=censo_id)
        except Censo.DoesNotExist:
            return Response(
                {'message': 'Entry not found in Censo.'},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            voto = Voto.objects.create(
                idCircunscripcion=data.get("idCircunscripcion"),
                idMesaElectoral=data.get("idMesaElectoral"),
                idProcesoElectoral=data.get("idProcesoElectoral"),
                nombreCandidatoVotado=data.get("nombreCandidatoVotado"),
                censo=censo
            )
        except Exception:
            return Response(
                {'message': 'Bad request, invalid data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if voto is None:
            return Response(
                {'message': 'Entry not found in Censo.'},
                status=status.HTTP_404_NOT_FOUND
            )

        voto_dict = model_to_dict(voto)
        voto_dict['marcaTiempo'] = str(voto.marcaTiempo)

        return Response(voto_dict, status=status.HTTP_200_OK)

    """
    API endpoint to delete a voto.
    """

    def delete(self, request, id_voto, format=None):
        if eliminar_voto(id_voto):
            return Response(
                {'message': 'Voto deleted successfully.'},
                status=status.HTTP_200_OK
            )
        else:
            return Response(
                {'message': 'Voto not found.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ProcesoElectoralView(APIView):
    """
    API endpoint to get a list of votos of a given idProcesoElectoral.
    """

    def get(self, request, idProcesoElectoral, format=None):
        # Filtramos los votos asociados al proceso electoral solicitado
        votos = get_votos_from_db(idProcesoElectoral)

        if votos.exists():
            # Si existen votos, los serializamos y los devolvemos
            votos_serializer = VotoSerializer(votos, many=True)
            return Response(votos_serializer.data, status=status.HTTP_200_OK)
        else:
            # Si no existen votos para el proceso electoral, devolvemos un
            # error
            return Response(
                {'message':
                    'No votes found for the specified electoral process.'},
                status=status.HTTP_404_NOT_FOUND
            )
