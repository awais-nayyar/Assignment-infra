import pika

# Establish a connection to RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

# Declare the camera-counts queue
channel.queue_declare(queue='camera-counts.py')

def on_message_callback(channel, method, properties, body):
    # Split the message into camera ID and event time
    message_parts = body.decode().split()
    camera_id = int(message_parts[0])
    event_time = message_parts[1]
    
    # Forward the number of cameras to detector
    # (You can replace this with your own code that sends the number to the detector)
    print(f"Camera ID: {camera_id}, Event time: {event_time}")

# Consume messages from the camera-counts queue
channel.basic_consume(queue='camera-counts.py', on_message_callback=on_message_callback, auto_ack=True)

# Start consuming messages
print('Waiting for camera counts...')
channel.start_consuming()

