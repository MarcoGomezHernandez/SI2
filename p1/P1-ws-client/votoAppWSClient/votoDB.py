# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# author: rmarabini
import requests
from django.conf import settings


def verificar_censo(censo_data):
    """ Check if the voter is registered in the Censo
    :param censo_dict: dictionary with the voter data
                       (as provided by CensoForm)
    :return True or False if censo_data is not valid
    """
    if bool(censo_data) is False:
        return False
    url = f"{settings.RESTAPIBASEURL}/censo/"
    response = requests.post(url, json=censo_data)
    return response.status_code == 200


def registrar_voto(voto_dict):
    """ Register a vote in the database
    :param voto_dict: dictionary with the vote data (as provided by VotoForm)
      plus de censo_id (numeroDNI) of the voter
    :return new voto info if succesful, None otherwise
    """
    url = f"{settings.RESTAPIBASEURL}/voto/"
    response = requests.post(url, json=voto_dict)
    if response.status_code == 200:
        return response.json()
    print(f"Error: Registrando voto: status code {response.status_code}")
    return None


def eliminar_voto(idVoto):
    """ Delete a vote in the database
    :param idVoto: id of the vote to be deleted
    :return True if succesful,
     False otherwise
     """
    url = f"{settings.RESTAPIBASEURL}/voto/{idVoto}/"
    response = requests.delete(url)
    return response.status_code == 200


def get_votos_from_db(idProcesoElectoral):
    """ Gets votes in the database correspondint to some electoral processs
    :param idProcesoElectoral: id of the vote to be deleted
    :return list of votes found
     """
    url = f"{settings.RESTAPIBASEURL}/proceso-electoral/{idProcesoElectoral}/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return []
