import pika

def callback(ch, method, properties, body):
    print('{}'.format(body.decode()))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='camera-events.py')

channel.basic_consume(queue='camera-events.py', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')

channel.start_consuming()

