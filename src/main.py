from ultralytics import YOLO
from area import area
from videoAnalyzer import videoAnalyzer
import cv2
import numpy as np
# da
# Paths
video_path = 'videos/SuperMarket.mp4'
model_path = 'models/yolov8x.pt'

# Load model
model = YOLO(model_path)

# Load video
cap = cv2.VideoCapture(video_path)

#start_frame = 500
#gcap.set(cv2.CAP_PROP_POS_FRAMES, start_frame) 

# Define areas
corridor_vertices = np.array([[267,326],[268,0],[0,0],[0,326]],np.int32)
exit_vertices = np.array([[360,0],[540,326],[580,326],[580,0]],np.int32)
register1_vertices = np.array([[269,290],[515,290],[520,326],[269,326]],np.int32)
register2_vertices = np.array([[270,154],[435,154],[504,282],[270,282]],np.int32)
register3_vertices = np.array([[270,80],[400,80],[427,143],[270,143]],np.int32)

corridor = area('corridor',color=(0,255,255),vertices=corridor_vertices)
exit = area('exit',color=(255,0,255),vertices=exit_vertices)
register1 = area('register1',color=(255,255,0),vertices=register1_vertices)
register2 = area('register2',color=(0,255,0),vertices=register2_vertices)
register3 = area('register3',color=(0,0,255),vertices=register3_vertices)

areasList = [corridor,exit,register1,register2,register3]

# Video properties
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

# Initialize video analyzer
video_analyzer = videoAnalyzer(areasList,height,width)

# frame counter
frameNumber = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)

    # process the video
    processed_frame = video_analyzer.processVideo(results,frameNumber,frame)

    # Display the resulting frame
    cv2.imshow('frame', processed_frame)
   
    # close if q, esc or close window button is pressed
    if cv2.waitKey(1) & 0xFF in [ord('q'), 27]:
        break
    
    # Update the frame number
    frameNumber += 1

cap.release()
cv2.destroyAllWindows()
