# Uses RabbitMQ as the server

import os
import sys
import django
import pika

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'votoSite.settings')
django.setup()

from votoAppRPCServer.models import Censo, Voto

def main():
    if len(sys.argv) != 3:
        print("Debe indicar el host y el puerto")
        exit()

    hostname = sys.argv[1]
    port = sys.argv[2]

    credentials = pika.PlainCredentials('alumnomq', 'alumnomq') # RabbitMQ credentials
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=hostname, port=port, credentials=credentials)) # Connect to RabbitMQ
    channel = connection.channel() # Create a channel

    channel.queue_declare(queue='voto_cancelacion') # Declare a queue

    # Callback function to handle incoming messages
    def callback(ch, method, properties, body):
        voto_id = int(body.decode()) # Get the vote ID from the message
        print(f"Received vote cancellation request for vote ID: {voto_id}")
        try:
            voto = Voto.objects.get(id=voto_id) # Get the vote object
            voto.codigoRespuesta = '111' # Set the response code to '111'
            voto.save() # Save the vote object
            print(f"Vote ID {voto_id} cancelled successfully.")
        except Voto.DoesNotExist:
            print(f"Vote ID {voto_id} does not exist.")

    channel.basic_consume(queue='voto_cancelacion', on_message_callback=callback, auto_ack=True) # Consume messages from the queue

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming() # Start consuming messages

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt: # Handle keyboard interrupt
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
