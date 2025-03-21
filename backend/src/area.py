import cv2
import numpy as np
class area:
    def __init__(self,name,color,vertices,actionNames):
        self.name = name
        self.color = color
        self.vertices = vertices
        self.IdsRecordInArea = set()
        self.currentIdsInArea = []
        self.currentNumberOfPeople = 0
        self.totalNumberOfPeople = 0
        self.actionCounter = self._buildActionCounter(actionNames)

    def isInside(self,point):
        vertices_np = np.array(self.vertices, dtype=np.int32)
        val =  cv2.pointPolygonTest(self.vertices,point,False)
        return val

    def _buildActionCounter(self,actionNames):
        actionCounter = {}
        for action in actionNames.values():
            actionCounter[action] = 0
        return actionCounter
    

    def drawArea(self,frame):
        # Desenha o polígono da área
        cv2.polylines(frame, [np.array(self.vertices)], True, self.color, 2)
        
        # Obtém os vértices do polígono
        vertices = np.array(self.vertices)
        
        # Encontra o ponto superior direito (menor y e maior x)
        top_right_point = vertices[np.argmin(vertices[:, 1])]  # Ponto com o menor y
        # Se houver múltiplos pontos com o mesmo y, escolha o que tem o maior x
        top_right_candidates = vertices[vertices[:, 1] == top_right_point[1]]
        top_right_point = top_right_candidates[np.argmin(top_right_candidates[:, 0])]
        
        # Define a posição do texto: abaixo e à direita do ponto superior direito
        text_x = top_right_point[0] + 5  # Mesmo x do ponto superior direito
        text_y = top_right_point[1] + 10  # Ajuste para colocar o texto abaixo do ponto

        # Escreve o nome da área e a quantidade de pessoas
        text = f'{self.name}'
        cv2.putText(frame, text, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
