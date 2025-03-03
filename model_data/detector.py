import cv2
import numpy as np
import time

np.random.seed(20)

class Detector:
    def __init__(self,videoPath, configPath, modelPath, classesPath):
        self.videoPath = videoPath
        self.configPath = configPath
        self.modelPath = modelPath
        self.classesPath = classesPath
        
        
        self.net = cv2.dnn_DetectionModel(self.modelPath, self.configPath)
        #Pre- processing before input images
        self.net.setInputSize(320,320) #Resizes input images which is expected size of the model
        self.net.setInputScale(1.0/127.5) # scales the pixel values to range [0,1] by dividing by 127.5
        self.net.setInputMean((127.5, 127.5, 127.5))  #normalize pixel value by subtratcting mean values
        self.net.setInputSwapRB(True)  #OpenCv uses BGR while most models uses RGB
        
        self.readClasses()
        
        
    def readClasses(self):
        with open(self.classesPath, 'r') as f:
            self.classesList = f.read().splitlines()
            
        self.classesList.insert(0, '__Background__')    
        
        self.colorList = np.random.uniform(low = 0, high = 255, size =(len(self.classesList), 3) )
            
        print(self.classesList)
        
    def onVideo(self):
        cap = cv2.VideoCapture(self.videoPath)
        
        if(cap.isOpened() == False):
            print('Error opening file...')
            return
        (success, image) = cap.read()
        
        startTime = 0
        
        while success:
            currentTime = time.time()
            fps = 1/(currentTime - startTime)
            startTime =currentTime
            classLabelIDs, confidences, bboxs =self.net.detect(image, confThreshold = 0.5 )
            
            bboxs = list(bboxs)
            confidences = list(map(float, confidences))
            
            # Non-Maximum Suppression (NMS) is used to filter out overlapping bounding boxes, keeping only the box with the highest confidence score for each object
            bboxIDx = cv2.dnn.NMSBoxes(bboxs, confidences, score_threshold= 0.5, nms_threshold= 0.2)
            # threshold value is used to eliminate bounding box that overlaps more than 20%
            
            if len(bboxIDx) != 0:
                for i in range(0, len(bboxIDx)):
                    
                    bbox = bboxs[np.squeeze(bboxIDx[i])]
                    classConfidence = confidences[np.squeeze(bboxIDx[i])]
                    classLabelID = np.squeeze(classLabelIDs[np.squeeze(bboxIDx[i])])
                    classLabel = self.classesList[classLabelID]
                    classColor = [int(c) for c in self.colorList[classLabelID]]
                    
                    displayText = "{}:{:.2f}".format(classLabel, classConfidence)
                    
                    x,y,w,h = bbox                 
                    
                    cv2.rectangle(image, (x,y), (x+w , y+h), color = classColor, thickness= 1)
                    
                    cv2.putText(image, displayText, (x,y-10), cv2.FONT_HERSHEY_PLAIN, 1, classColor,2 )
                    
                    
                    lineWidth = min(int(w * 0.3), int(h * 0.3))
                    cv2.line(image, (x,y),(x + lineWidth, y), classColor, thickness= 5)
                    cv2.line(image, (x,y),(x , y + lineWidth), classColor, thickness= 5)
                    
                    cv2.line(image, (x + w,y),(x + w - lineWidth, y), classColor, thickness= 5)
                    cv2.line(image, (x + w,y),(x + w , y + lineWidth), classColor, thickness= 5)
                    
                   #----------------------------------------------# 
                    cv2.line(image, (x,y + h),(x + lineWidth, y + h), classColor, thickness= 5)
                    cv2.line(image, (x,y + h),(x , y + h - lineWidth), classColor, thickness= 5)
                    
                    cv2.line(image, (x + w,y + h),(x + w - lineWidth, y + h), classColor, thickness= 5)
                    cv2.line(image, (x + w,y + h),(x + w , y + h - lineWidth), classColor, thickness= 5)
                    
            cv2.putText(image,"FPS:" +str(int(fps)),(20,70), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,0), 2)
            cv2.imshow("Result", image)
            
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            (success, image) = cap.read()
        cv2.destroyAllWindows()
            
            