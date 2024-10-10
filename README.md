# Object-Detection using OpenCV
This repository contains code to perform object detection using a pre-trained deep learning model with OpenCV's dnn module. It reads a video file, detects objects, and draws bounding boxes with labels around detected objects. The project also computes the frame-per-second (FPS) value to show real-time detection performance.

## Features 
- Object detection using deep learning with OpenCV's DNN module.
- Non-Maximum Suppression (NMS) for eliminating overlapping bounding boxes.
- Display bounding boxes and class labels with confidence scores.
- FPS calculation for performance measurement.
- Customizable model, configuration, and class file paths.
## Installation
1 Clone the repository:
  git clone https://github.com/Yukti007/Object-Detection.git
2 Install the required dependencies:
  pip install opencv-python opencv-python-headless numpy
  
3 Ensure you have the following files:

- Pre-trained Model (e.g., .weights or .caffemodel)
- Model Configuration (e.g., .cfg file)
- Class Labels (e.g., .txt file containing the names of classes)
