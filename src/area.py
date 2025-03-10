import cv2
import numpy as np
class area:
    def __init__(self,name,color,vertices):
        self.name = name
        self.color = color
        self.vertices = vertices
        self.IdsRecordInArea = set()
        self.currentIdsInArea = []
        self.currentNumberOfPeople = 0
        self.totalNumberOfPeople = 0

    def isInside(self,point):
        vertices_np = np.array(self.vertices, dtype=np.int32)
        val =  cv2.pointPolygonTest(self.vertices,point,False)
        return val
