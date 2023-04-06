import threading
import time
import random
import datetime
import pika

class CameraEmulator(threading.Thread):
    def __init__(self, camera_id):
        super(CameraEmulator, self).__init__()
        self.camera_id = camera_id
        self.is_online = True
        self.offline_duration = 0

    def run(self):
        while True:
            if self.is_online:
                #event_time = datetime.datetime.now()
                event_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                event_message = f"Camera ID: {self.camera_id} - Time: {event_time} {self.get_random_string()}"
                print(event_message)
                self.publish_to_camera_events_queue(event_message)
                self.publish_to_camera_counts_queue(self.camera_id, event_time)

            time.sleep(random.randint(10, 110))

            

            # Randomly go offline for a random duration (> 2 minutes)
            if random.random() < 0.1:
                print(f"Camera {self.camera_id} is offline")
                offline_duration = random.randint(120, 600)
                time.sleep(offline_duration)
                print(f"Camera {self.camera_id} is back online")
    
    def stop(self):
        self.is_running = False
    def get_random_string(self, length=10):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        return ''.join(random.choice(letters) for i in range(length))

    def publish_to_camera_events_queue(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='camera-events.py')
        channel.basic_publish(exchange='', routing_key='camera-events.py', body=message)
        connection.close()

    def publish_to_camera_counts_queue(self, camera_id, event_time):
        message = f" {camera_id} {event_time}"
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='camera-counts.py')
        channel.basic_publish(exchange='', routing_key='camera-counts.py', body=message)
        connection.close()

if __name__ == '__main__':
    num_cameras = 100
    threads = []
    for i in range(num_cameras):
        thread = CameraEmulator(i)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()
