import pika
import sys

def cancelar_voto(hostname, port, id_voto):
    try:
        # conectar con rabbitMQ
        credentials = pika.PlainCredentials('alumnomq', 'alumnomq') # RabbitMQ credentials
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)) # Connect to RabbitMQ
        channel = connection.channel() # Create a channel
    except Exception:
        print("Error al conectar al host remoto")
        exit()

    # declarar cola y publicar mensaje
    channel.queue_declare(queue='voto_cancelacion')
    channel.basic_publish(exchange='',
                          routing_key='voto_cancelacion',
                          body=id_voto)

    # cerrar conexión
    connection.close()

def main():
    if len(sys.argv) != 4:
        print("Debe indicar el host, el número de puerto y el ID del voto a cancelar como argumento.")
        exit()

    cancelar_voto(sys.argv[1], sys.argv[2], sys.argv[3])

if __name__ == "__main__":
    main()
