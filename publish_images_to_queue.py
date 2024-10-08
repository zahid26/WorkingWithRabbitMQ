"""
    Task: Publish message(images/frames) to rabbitmq.
    Author: Zahid Alaie.
    Last Updated on: 07-October-2024 

"""

import pika
import base64
import os
import numpy as np
import cv2
from loguru import logger
from ultralytics import YOLO
import time

model = YOLO("yolov8s.pt")

def connect_rabbitmq():
    """Connect to RabbitMQ"""
    connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.1.145'))
    channel = connection.channel()
    channel.queue_declare(queue='image_queue')
    return channel, connection

def image_to_base64(image_path):
    """Convert an image file to Base64 string"""
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_string

def publish_image(channel, base64_string, image_name):
    """Publish Base64-encoded image to the RabbitMQ queue"""
    message = {
        'image_name': image_name,
        'image_data': base64_string
    }

    channel.basic_publish(exchange='',
                          routing_key='image_queue',
                          body=str(message))
    logger.info(f"Image {image_name} sent to queue!")

def process_images_in_folder(folder_path):
    """Process all images in the folder and send them to the RabbitMQ queue"""
    channel, connection = connect_rabbitmq()

    for image_file in os.listdir(folder_path):
        image_path = os.path.join(folder_path, image_file)

        if os.path.isfile(image_path) and image_file.lower().endswith(('png', 'jpg', 'jpeg')):
            base64_string = image_to_base64(image_path)
            publish_image(channel, base64_string, image_file)
    connection.close()


if __name__ == '__main__':
    folder_path = r"C:\Users\zahid\Desktop\General\test_images\persons"

    process_images_in_folder(folder_path)
