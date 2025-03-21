from area import area
from person import person
from heatMap import heatMap
from stats import stats
from trajectoryGraph import trajectoryGraph
from spaghetti import Spaghetti
import cv2
import numpy as np


class videoAnalyzer:
    def __init__(self,areasList,height,width,classNames,filename='stats'):
        self.id = 0
        self.areasDict = self._buildAreasDict(areasList)
        self.people = {}
        self.classNames = classNames
        self.heatmap = heatMap(height,width)
        self.statistics = stats(self.people,self.areasDict,filename)
        self.trajGraph= trajectoryGraph(areasList,height,width)
        self.spaghetti = Spaghetti((height,width))


    def _buildAreasDict(self,areasList):
        areasDict = {}
        for area in areasList:
            areasDict[area.name] = area
        return areasDict
        
    # Return tuple of BBOx,centroids and class name
    def getData(self,results):
        data = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            cls_name = self.classNames[cls]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            data.append(((x1, y1, x2, y2), ((x1 + x2) // 2, (y1 + y2) // 2),cls_name))
        return data
    

    def removeLostPeople(self,frameNumber):
        to_remove = []
        for id,_person in self.people.items():
            if frameNumber - _person.lastFrameDetected > 10:
                to_remove.append(id)
        
        for id in to_remove:
            del self.people[id]
        


    def updatePeopleDict(self,results,frameNumber,threshold = 20):
        # get Bbox and centroids
        data = self.getData(results)
        # Check if one of the centroides corresponds to a person in the dictionary
        # based on the euclidean distance
        for coordinates,centroid,cls_name in data:
            current_threshold = threshold
            closest_person = None
            for _,previous_person in self.people.items():
                distance = previous_person.dist2centroid(centroid)
                if distance is not None and distance < current_threshold:
                    current_threshold = distance
                    closest_person = previous_person.id
            # If the centroid is close to a person in the dictionary, update the position of the person
            if closest_person is not None:
                self.people[closest_person].updatePosition(coordinates,centroid)
                # Update Spaghetti
                self.spaghetti.update(self.people[closest_person],self.areasDict)
                self.people[closest_person].lastFrameDetected = frameNumber
                self.people[closest_person].action = cls_name
                self.people[closest_person].actionCounter[cls_name] += 1
            # If the centroid wasn't close to any person in the dictionary, create a new person
            else:
                self.id += 1
                self.people[self.id] = person(self.id,frameNumber,self.areasDict,self.classNames,cls_name)
                self.people[self.id].updatePosition(coordinates,centroid)
                self.spaghetti.update(self.people[self.id],self.areasDict)
                self.people[self.id].actionCounter[cls_name] += 1


    def updatePersonArea(self):
        for person in self.people.values():
            for _area in self.areasDict.values():
                val = _area.isInside(person.positionHistory[-1])
                # val is positive if person`s centroid is inside the area
                if val > 0:
                    person.currentArea = _area.name
                    person.BBoxColor = _area.color
                    person.framesSpentinArea[_area.name] += 1

                    # Update person`s actionsPerAreaMatrix
                    i = person.areaToNumber[_area.name]
                    j = person.actionToNumber[person.action]
                    person.actionsPerAreaMatrix[i][j] += 1

                    # Checks if person`s visited areas list is empty
                    if len(person.visitedAreas) == 0:
                        person.visitedAreas.append(_area.name)
                        break
                    else:
                        if person.visitedAreas[-1] != person.currentArea:
                            person.visitedAreas.append(_area.name)
                            if len(person.visitedAreas) >= 2:
                                self.trajGraph.updateIncidenceMatrix(person.visitedAreas[-2],person.visitedAreas[-1])
                            break
                            
                            
    

    def updateAreas(self):
        for id,_person in self.people.items():
            if _person.currentArea is not None:
                self.areasDict[_person.currentArea].currentIdsInArea.append(id)
                self.areasDict[_person.currentArea].IdsRecordInArea.add(id)
                self.areasDict[_person.currentArea].currentNumberOfPeople += 1
                self.areasDict[_person.currentArea].totalNumberOfPeople = len(self.areasDict[_person.currentArea].IdsRecordInArea)
                self.areasDict[_person.currentArea].actionCounter[_person.action] += 1

    
    def drawBoundingBoxes(self,frame):
        for _person in self.people.values():
            _person.drawBoundingBox(frame)
        return frame
    

    def drawAreas(self, frame):
        for _area in self.areasDict.values():
            _area.drawArea(frame)
        return frame

    
    def buildHeatMap(self,frame):
        for _person in self.people.values():
            self.heatmap.updateDetectionMatrix(_person.BBox)
        
        overlayedHeatMap = self.heatmap.overlayHeatMap(frame)
        return overlayedHeatMap
    
    def clearAreaCurrentInfo(self):
        for _area in self.areasDict.values():
            _area.currentNumberOfPeople = 0
            _area.currentIdsInArea = []
    

    def processVideo(self,results,frameNumber,frame):
        frameCopy = frame.copy()
        frameCopy = self.drawAreas(frameCopy)

        self.removeLostPeople(frameNumber)
        self.updatePeopleDict(results,frameNumber)
        self.updatePersonArea()
        self.updateAreas()
        frame = self.buildHeatMap(frame)
        frame = self.drawAreas(frame)
        frame = self.drawBoundingBoxes(frame)
        
        '''
        # print number of people in each area:
        for _area in self.areasDict.values():
            print(f'{_area.name}: {_area.currentNumberOfPeople}')

        # plot line following each person`s centroid
        for _person in self.people.values():
            for i in range(len(_person.positionHistory) - 1):
                cv2.line(frame, _person.positionHistory[i], _person.positionHistory[i + 1], _person.BBoxColor, 2)
        '''
        self.statistics.updateAreasStats()  
        self.statistics.updatePeopleStats()
        self.statistics.createAreasCSV()
        self.statistics.createPersonCSV()
        #self.statistics.generateReport(frameNumber)
        self.spaghetti.drawSpaghetti(frameCopy)
        #self.trajGraph.drawSpaghettiDiagram(frameCopy)

        self.clearAreaCurrentInfo()

        return frame

    

                