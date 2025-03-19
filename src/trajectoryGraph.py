import cv2
import numpy as np
from area import area

class trajectoryGraph:
    def __init__(self,areasList,height,width):
        self.areasList = areasList
        self.height = height
        self.width = width
        self.centroids = self.getAreaCentroids()
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
        for i, _area in enumerate(self.areasList):
            areaToNumber[_area.name] = i
            numberToArea[i] = _area.name
        return areaToNumber, numberToArea
    

    def updateIncidenceMatrix(self,starArea,endArea):
        i = self.areaToNumber[starArea]
        j = self.areaToNumber[endArea]


        self.incidenceMatrix[i][j] += 1 



    def drawSpaghettiDiagram(self, frame):
        # Criar uma cópia da imagem de fundo para desenhar o diagrama
        diagram = frame.copy()

        # Desenhar os centróides
        for (x, y), color in self.centroids.values():
            cv2.circle(diagram, (x, y), 10, color, -1)  # Desenha o centróide

            # Desenhar as arestas direcionadas com base na incidenceMatrix
            for i in range(len(self.areasList)):
                for j in range(len(self.areasList)):
                    if self.incidenceMatrix[i, j] > 0 and i != j:  # Existe uma transição entre as áreas
                        start_point = self.centroids[self.numberToArea[i]][0]  # Coordenadas do nó de origem
                        end_point = self.centroids[self.numberToArea[j]][0]  # Coordenadas do nó de destino

                        # Desenhar a aresta
                        thickness = int(1 + self.incidenceMatrix[i, j] // 5)  # Espessura baseada na frequência
                        cv2.line(diagram, start_point, end_point, (0, 0, 255), thickness, cv2.LINE_AA)

                        # Adicionar seta para indicar a direção do fluxo
                        mid_x = (start_point[0] + end_point[0]) // 2
                        mid_y = (start_point[1] + end_point[1]) // 2
                        cv2.arrowedLine(diagram, start_point, (mid_x, mid_y), (0, 0, 255), thickness, tipLength=0.2)

            # Exibir o diagrama
            cv2.imshow("Spaghetti Diagram", diagram)
            cv2.waitKey(1)  # Atualiza a janela continuamente
