import cv2
import numpy as np

class heatMap:
    def __init__(self, height, width, decay=0.99):
        self.height = height
        self.width = width
        self.decay = decay
        self.detectionMatrix = np.zeros((height, width), dtype=np.float32)
    
    def applyDecay(self):
        self.detectionMatrix *= self.decay
    
    def updateDetectionMatrix(self, bbox):
        x1, y1, x2, y2 = bbox
        
        # Atualiza os valores usando a escala logarítmica
        self.detectionMatrix[y1:y2, x1:x2] += 1  # Incrementa normalmente
        #self.detectionMatrix[y1:y2, x1:x2] = np.log1p(self.detectionMatrix[y1:y2, x1:x2])  # Aplica log

    def getNormalizedDetectionMatrix(self):
        # Normaliza os valores para o intervalo 0-255
        normalizedMatrix = np.zeros_like(self.detectionMatrix)
        cv2.normalize(self.detectionMatrix, normalizedMatrix, 0, 255, cv2.NORM_MINMAX)
        normalizedMatrix = 255 - normalizedMatrix  # Inverte para que azul seja menos e vermelho seja mais
        return normalizedMatrix.astype(np.uint8)

    def getColoredHeatMap(self):
        normalizedMatrix = self.getNormalizedDetectionMatrix()
        heatmap = cv2.applyColorMap(normalizedMatrix, cv2.COLORMAP_JET)  # Aplica o colormap
        return heatmap

    def overlayHeatMap(self, frame):
        self.applyDecay()  # Aplica o decay a cada iteração para suavizar a transição
        heatmap = self.getColoredHeatMap()
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)  # Converte para o formato correto
        output = cv2.addWeighted(frame, 0.5, heatmap, 0.5, 0)
        return output
