from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import VotoSerializer
from .models import Censo, Voto
from django.forms.models import model_to_dict


class CensoView(APIView):
    """
    API endpoint to collect censo information.
    and check if the person is in the censo.
    """

    def post(self, request, format=None):
        data = request.data

        numero_dni = data.get('numeroDNI')
        nombre = data.get('nombre')
        fecha_nacimiento = data.get('fechaNacimiento')
        codigo_autorizacion = data.get('codigoAutorizacion')

        try:
            censo = Censo.objects.get(numeroDNI=numero_dni)

            if ((censo.nombre == nombre)
                    and (censo.fechaNacimiento == fecha_nacimiento)
                    and (censo.codigoAutorizacion == codigo_autorizacion)):
                return Response({'message': 'Datos encontrados en Censo.'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Datos no encontrados en Censo.'},
                                status=status.HTTP_404_NOT_FOUND)
        except Censo.DoesNotExist:
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
        except Exception as e:
            return Response(
                {'message': 'Error creating Voto: {}'.format(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

        if voto is None:
            return Response(
                {'message': 'Entry not found in Censo.'},
                status=status.HTTP_404_NOT_FOUND
            )

        voto_dict = model_to_dict(voto)
        return Response(voto_dict, status=status.HTTP_200_OK)

    """
    API endpoint to delete a voto.
    """

    def delete(self, request, id_voto, format=None):
        # Intentamos obtener el voto a eliminar por su identificador
        try:
            voto = Voto.objects.get(id=int(id_voto))
        except Voto.DoesNotExist:
            # Si el voto no existe, devolvemos un error con estado
            # HTTP_404_NOT_FOUND
            return Response(
                {'message': 'Voto not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Si el voto existe, lo eliminamos
        voto.delete()

        # Devolvemos una respuesta con el estado HTTP_200_OK
        return Response(
            {'message': 'Voto deleted successfully.'},
            status=status.HTTP_200_OK
        )


class ProcesoElectoralView(APIView):
    """
    API endpoint to get a list of votos of a given idProcesoElectoral.
    """

    def get(self, request, idProcesoElectoral, format=None):
        # Filtramos los votos asociados al proceso electoral solicitado
        votos = Voto.objects.filter(idProcesoElectoral=idProcesoElectoral)

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
