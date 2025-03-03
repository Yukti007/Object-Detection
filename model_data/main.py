from detector import *
import os


def main():
    videoPath = 0 #'test_videos/test1.mp4' #for webcam we can  replace with 0
    
    configPath = os.path.join('model_data', 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt')
    
    modelPath = os.path.join('model_data','frozen_inference_graph.pb')
    
    classesPath = os.path.join('model_data', 'coco.names')
    
    detector = Detector(videoPath, configPath, modelPath, classesPath)
    detector.onVideo()
    
if __name__ == '__main__':
    main()