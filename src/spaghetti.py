import cv2
import numpy as np
from area import area

class spaghetti:
    def __init__(self,areasList,height,width):
        self.areasList = areasList
        self.height = height
        self.width = width
        areaCentroids = self.getAreaCentroids()
        self.areaToNumber,self.numberToArea = self.buildMapping()
        self.incidenceMatrix = np.zeros((len(areasList),len(areasList)))
    

    def getAreaCentroids(self):
        centroids = {}
        for area in self.areasList:
            vertices = area.vertices  # Obtém os vértices da área (array NumPy)
            
            minX = np.min(vertices[:, 0])  # Menor valor de X
            maxX = np.max(vertices[:, 0])  # Maior valor de X
            minY = np.min(vertices[:, 1])  # Menor valor de Y
            maxY = np.max(vertices[:, 1])  # Maior valor de Y

            centroid_x = (minX + maxX) // 2  # Centro X da área
            centroid_y = (minY + maxY) // 2  # Centro Y da área

            centroid_color = area.color

            centroids[area.name] = ((centroid_x, centroid_y),centroid_color)
        
        return centroids

    def buildMapping(self):
        areaToNumber = {}
        numberToArea = {}
        for i, area.name in enumerate(self.areasList):
            areaToNumber[area.name] = i
            numberToArea[i] = area.name
        return areaToNumber, numberToArea



    def drawSpaghettiDiagram(self,frame):
        pass