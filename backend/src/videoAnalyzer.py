from area import area
from person import person
from heatMap import heatMap
from stats import stats
from trajectoryGraph import trajectoryGraph
from spaghetti import Spaghetti
import cv2
import numpy as np


class videoAnalyzer:
    def __init__(self,areasList,height,width,classNames,filename='backend/stats'):
        self.id = 0
        self.areasDict = self._buildAreasDict(areasList)
        self.people = {}
        self.classNames = classNames
        self.heatmap = heatMap(height,width)
        self.statistics = stats(self.people,self.areasDict,filename)
        self.trajGraph= trajectoryGraph(areasList,height,width)
        self.spaghetti = Spaghetti((height,width))

    # Constrói um dicionário com as áreas
    def _buildAreasDict(self,areasList):
        areasDict = {}
        for area in areasList:
            areasDict[area.name] = area
        return areasDict
        
    # Retorna a BBox, o centróide e a ação detectada
    def getData(self,results):
        data = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            cls_name = self.classNames[cls]
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            data.append(((x1, y1, x2, y2), ((x1 + x2) // 2, (y1 + y2) // 2),cls_name))
        return data
    
    # Remove pessoas que não foram detectadas por um certo número de frames
    def removeLostPeople(self,frameNumber):
        to_remove = []
        for id,_person in self.people.items():
            if frameNumber - _person.lastFrameDetected > 10:
                to_remove.append(id)
        
        for id in to_remove:
            del self.people[id]
        

    # Atualiza o dicionário de pessoas
    def updatePeopleDict(self,results,frameNumber,threshold = 20):
        # Obtém a BBox, o centróide e a ação detectada
        data = self.getData(results)
        # Confere se o centróide está proximo de alguma pessoa no dicionário
        # Com base na menor distância entre os centróides
        for coordinates,centroid,cls_name in data:
            current_threshold = threshold
            closest_person = None
            for _,previous_person in self.people.items():
                distance = previous_person.dist2centroid(centroid)
                if distance is not None and distance < current_threshold:
                    current_threshold = distance
                    closest_person = previous_person.id
            # Se o centróide está próximo de alguma pessoa no dicionário, atualiza a posição
            if closest_person is not None:
                self.people[closest_person].updatePosition(coordinates,centroid)
                # Update Spaghetti
                self.spaghetti.update(self.people[closest_person],self.areasDict)
                self.people[closest_person].lastFrameDetected = frameNumber
                self.people[closest_person].action = cls_name
                self.people[closest_person].actionCounter[cls_name] += 1
            # Caso contrário, cria uma nova pessoa
            else:
                self.id += 1
                self.people[self.id] = person(self.id,frameNumber,self.areasDict,self.classNames,cls_name)
                self.people[self.id].updatePosition(coordinates,centroid)
                self.spaghetti.update(self.people[self.id],self.areasDict)
                self.people[self.id].actionCounter[cls_name] += 1

    # Atualiza a área atual de cada pessoa
    def updatePersonArea(self):
        for person in self.people.values():
            for _area in self.areasDict.values():
                val = _area.isInside(person.positionHistory[-1])
                # val é positivo caso o centróide esteja dentro da área
                if val > 0:
                    person.currentArea = _area.name
                    person.BBoxColor = _area.color
                    person.framesSpentinArea[_area.name] += 1

                    # Atualiza a matriz de ações por área da pessoa
                    i = person.areaToNumber[_area.name]
                    j = person.actionToNumber[person.action]
                    person.actionsPerAreaMatrix[i][j] += 1

                    # Confere se a lista de áreas visitadas da pessoa está vazia
                    if len(person.visitedAreas) == 0:
                        person.visitedAreas.append(_area.name)
                        break
                    else:
                        if person.visitedAreas[-1] != person.currentArea:
                            person.visitedAreas.append(_area.name)
                            if len(person.visitedAreas) >= 2:
                                self.trajGraph.updateIncidenceMatrix(person.visitedAreas[-2],person.visitedAreas[-1])
                            break
                            
                            
    
    # Atualiza as informações das áreas
    def updateAreas(self):
        for id,_person in self.people.items():
            if _person.currentArea is not None:
                self.areasDict[_person.currentArea].currentIdsInArea.append(id)
                self.areasDict[_person.currentArea].IdsRecordInArea.add(id)
                self.areasDict[_person.currentArea].currentNumberOfPeople += 1
                self.areasDict[_person.currentArea].totalNumberOfPeople = len(self.areasDict[_person.currentArea].IdsRecordInArea)
                self.areasDict[_person.currentArea].actionCounter[_person.action] += 1

    # Desenha as bounding boxes das pessoa no frame
    def drawBoundingBoxes(self,frame):
        for _person in self.people.values():
            _person.drawBoundingBox(frame)
        return frame
    
    # Desenha o contorno das áreas no frame
    def drawAreas(self, frame):
        for _area in self.areasDict.values():
            _area.drawArea(frame)
        return frame

    # Constrói o heatmap
    def buildHeatMap(self,frame):
        for _person in self.people.values():
            self.heatmap.updateDetectionMatrix(_person.BBox)
        
        overlayedHeatMap = self.heatmap.overlayHeatMap(frame)
        return overlayedHeatMap
    
    # Limpa as informações atuais das áreas
    def clearAreaCurrentInfo(self):
        for _area in self.areasDict.values():
            _area.currentNumberOfPeople = 0
            _area.currentIdsInArea = []
    
    # Processa o vídeo
    def processVideo(self,results,frameNumber,frame):
        self.removeLostPeople(frameNumber)
        self.updatePeopleDict(results,frameNumber)
        self.updatePersonArea()
        self.updateAreas()
        
        
        self.statistics.updateAreasStats()  
        self.statistics.updatePeopleStats()
        self.statistics.createAreasCSV()
        self.statistics.createPersonCSV()

        self.clearAreaCurrentInfo()

        return frame
    

    def createHeatMap(self,frame):
        frameCopy = frame.copy()
        heatMap = self.buildHeatMap(frameCopy)
        heatMap = self.drawAreas(heatMap)
        heatMap = self.drawBoundingBoxes(heatMap)
        return heatMap
    
    def createSpaghetiDiagram(self,frame):
        frameCopy = frame.copy()
        spaghettiDiagram = self.spaghetti.drawSpaghetti(frameCopy)
        spaghettiDiagram = self.drawAreas(spaghettiDiagram)
        return spaghettiDiagram
    
    def createTrajectoryGraph(self,frame):
        frameCopy = frame.copy()
        trajectoryGraph = self.trajGraph.drawGraph(frameCopy)
        trajectoryGraph = self.drawAreas(trajectoryGraph)
        return trajectoryGraph

    
    def rawFrame(self,frame):
        return frame
    


    

                