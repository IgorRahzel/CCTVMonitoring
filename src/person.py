import numpy as np
import cv2
from collections import deque

class person:
    def __init__(self,id,frameNumber,areasDict,actionNames,action=None,maxHistory=30):
        self.id = id
        self.action = action
        self.actionCounter = self._buildActionCounter(actionNames)
        self.positionHistory = deque(maxlen=maxHistory)
        self.visitedAreas = []
        self.currentArea = None
        self.BBox = None
        self.BBoxColor = None
        self.framesSpentinArea = self._initFramesSpentInArea(areasDict)
        self.lastFrameDetected = frameNumber
        self.areaToNumber,self.numberToArea = self._buildMappingForAreas(areasDict)
        self.actionToNumber, self.numberToAction = self._buildMappingForActions(actionNames)
        self.actionsPerAreaMatrix = np.zeros((len(areasDict),len(actionNames)),dtype=np.int32)

    def _initFramesSpentInArea(self,areasDict):
        framesSpentInArea = {}
        for area in areasDict.values():
            framesSpentInArea[area.name] = 0
        return framesSpentInArea
    
    def _buildMappingForAreas(self,areasDict):
        areaToNumber = {}
        numberToArea = {}
        for i, _area in enumerate(areasDict.values()):
            areaToNumber[_area.name] = i
            numberToArea[i] = _area.name
        return areaToNumber, numberToArea
    
    def _buildMappingForActions(self,actionNames):
        actionToNumber = {}
        numberToAction = {}
        for i, action in enumerate(actionNames.values()):
            actionToNumber[action] = i
            numberToAction[i] = action
        return actionToNumber, numberToAction
    
    def _buildActionCounter(self,actionNames):
        actionCounter = {}
        for action in actionNames.values():
            actionCounter[action] = 0
        return actionCounter
        
    
    def dist2centroid(self,centroid):
        if len(self.positionHistory) > 0:
            last_position = self.positionHistory[-1]
            distance = np.linalg.norm(np.array(centroid) - np.array(last_position))
            return distance
        
        return None
    
    def drawBoundingBox(self,frame):
            x1,y1,x2,y2 = self.BBox
            cv2.rectangle(frame, (x1, y1), (x2, y2), self.BBoxColor, 2)
            cv2.putText(frame, f'id:{self.id} {self.action}', (x1, y1-3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            
    def updatePosition(self,bbox,centroid):
        self.BBox = bbox
        self.positionHistory.append(centroid)
        

        