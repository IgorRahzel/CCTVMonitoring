import numpy as np
import cv2
from collections import deque

class person:
    def __init__(self,id,frameNumber,areasDict,maxHistory=30):
        self.id = id
        self.positionHistory = deque(maxlen=maxHistory)
        self.visitedAreas = []
        self.currentArea = None
        self.BBox = None
        self.BBoxColor = None
        self.framesSpentinArea = self._initFramesSpentInArea(areasDict)
        self.lastFrameDetected = frameNumber

    def _initFramesSpentInArea(self,areasDict):
        framesSpentInArea = {}
        for area in areasDict.values():
            framesSpentInArea[area.name] = 0
        return framesSpentInArea
    
    def dist2centroid(self,centroid):
        if len(self.positionHistory) > 0:
            last_position = self.positionHistory[-1]
            distance = np.linalg.norm(np.array(centroid) - np.array(last_position))
            return distance
        
        return None
    
    def drawBoundingBox(self,frame):
            x1,y1,x2,y2 = self.BBox
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.BBoxColor, 2)
            cv2.putText(frame, f'id:{self.id}', (x1, y1-3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
    
    def updatePosition(self,bbox,centroid):
        self.BBox = bbox
        self.positionHistory.append(centroid)
        

        