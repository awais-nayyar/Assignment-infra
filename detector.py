import pika
import datetime

class Camera:
    def __init__(self, id, last_seen):
        self.id = id
        self.last_seen = last_seen
        self.is_offline = False

class Detector:
    def __init__(self):
        self.cameras = {}
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='camera-counts.py')
        
    def start(self):
        self.channel.basic_consume(queue='camera-counts.py', on_message_callback=self.callback, auto_ack=True)
        print('Detector started. Waiting for camera events...')
        self.channel.start_consuming()
        
    def stop(self):
        self.channel.stop_consuming()
        self.connection.close()
        
    def callback(self, ch, method, properties, body):
        message_parts = body.decode().split()
        camera_id = int(message_parts[0])
        event_time = message_parts[1]
        
        if camera_id not in self.cameras:
            self.cameras[camera_id] = Camera(camera_id, datetime.datetime.now())
            
        self.cameras[camera_id].last_seen = datetime.datetime.now()
        
        if self.cameras[camera_id].is_offline:
            offline_duration = datetime.datetime.now() - self.cameras[camera_id].last_seen
            if offline_duration.total_seconds() > 120:
                print(f"Camera {camera_id} has been offline for {offline_duration.total_seconds()} seconds")
    
        # Check for offline cameras
        for camera_id, camera in self.cameras.items():
            time_since_last_seen = datetime.datetime.now() - camera.last_seen
            if time_since_last_seen.total_seconds() > 120 and not camera.is_offline:
                camera.is_offline = True
                offline_duration = time_since_last_seen.total_seconds()
                print(f"Camera {camera_id} is offline. Last seen {int(time_since_last_seen.total_seconds())} seconds ago.")
            elif time_since_last_seen.total_seconds() <= 120 and camera.is_offline:
                camera.is_offline = False
                print(f"Camera {camera_id} is back online.")

                
if __name__ == '__main__':
    detector = Detector()
    detector.start()

