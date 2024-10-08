"""
    Task: Consume the messages(images/frames) from queue and do inference, here using Yolov8.
    Author: Zahid Alaie.
    Last Updated on: 07-October-2024 

"""

import pika
import base64
import cv2
import numpy as np
from ultralytics import YOLO
import time
from loguru import logger

model = YOLO("yolov8s.pt")

def connect_rabbitmq():
    """Connect to RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='image_queue')
    return channel, connection

def base64_to_image_array(base64_string):
    """Convert Base64 string back to image array"""
    image_data = base64.b64decode(base64_string)
    np_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    return img

def callback(ch, method, properties, body):
    """Callback function that processes the message"""
    message = eval(body.decode('utf-8'))
    image_name = message['image_name']
    base64_string = message['image_data']

    img_array = base64_to_image_array(base64_string)

    if img_array is not None:
        logger.info(f"Received and converted image {image_name} to array and performing Inference!")

        res = model.predict(img_array, classes=[0])

        print(res[0].boxes.xyxy.numpy())
        # do necessary processing here.

    else:
        logger.error(f"Failed to convert image {image_name}")

def check_empty_queue(channel):
    """Check if the queue is empty"""
    queue_state = channel.queue_declare(queue='image_queue', passive=True)
    return queue_state.method.message_count == 0

def start_consumer():
    """Start the RabbitMQ consumer to process image data and auto-exit when queue is empty"""
    channel, connection = connect_rabbitmq()

    while True:
        if check_empty_queue(channel):
            logger.info('Queue is empty. Exiting...')
            break 
        method_frame, properties, body = channel.basic_get(queue='image_queue')

        if method_frame:
            callback(channel, method_frame, properties, body)
            channel.basic_ack(method_frame.delivery_tag)
        else:
            logger.warning('No message received, waiting...')
            time.sleep(1)
    connection.close()

if __name__ == '__main__':
    start_consumer()
