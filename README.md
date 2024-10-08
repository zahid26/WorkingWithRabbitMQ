
# Working With rabbitmq

This project consists of two Python scripts designed to handle messages related to inference and publish images to a message queue. Below is an overview of each script and how to use them.

## Files Overview

### 1. `consume_inference_messages.py`
This script is responsible for consuming messages related to inference. It listens to a queue, retrieves messages, and processes the inference results.

#### Features
- Connects to a message queue.
- Retrieves inference-related messages.
- Processes the data for further analysis.

#### Usage
```bash
python consume_inference_messages.py
```

### 2. `publish_images_to_queue.py`
This script handles the task of publishing images to a message queue. It reads images from a specified directory and publishes them to the queue for further processing.

#### Features
- Reads images from a local directory.
- Publishes images to a queue for processing.

#### Usage
```bash
python publish_images_to_queue.py
```

## Prerequisites

- Python 3.x
- Pika
- Opencv-Python
- Ultralytics
- Numpy
- Loguru
- os

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/project.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

