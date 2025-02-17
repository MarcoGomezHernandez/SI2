# read the first 1000 entries
# then perform 1000 queries retrieving each one of the entries
# one by one. Measure the time requiered for the 1000 queries

import time
import os
import django


try:
    # Configurar el entorno de Django
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "votoSite.settings")
    django.setup()

    # Importar el modelo Censo
    from votoAppWSServer.models import Censo

    # Leer las claves primarias de las primeras 1000 entradas de Censo
    censo_pks = [censo_entrie.numeroDNI for censo_entrie in Censo.objects.all()[:1000]]

    # Medir el tiempo de inicio
    start_time = time.time()

    # Realizar busquedas una a una
    for censo_pk in censo_pks:
        Censo.objects.get(pk=censo_pk)

    # Medir el tiempo de finalizacion
    end_time = time.time()

    # Mostrar los resultados
    print(f"Tiempo invertido en buscar las 1000 entradas una a una: {end_time - start_time:.6f} segundos")

except Exception as e:
    print(f"Error: {e}")
