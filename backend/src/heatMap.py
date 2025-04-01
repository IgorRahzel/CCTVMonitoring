import cv2
import numpy as np

class heatMap:
    def __init__(self, height, width, decay=0.99):
        self.height = height
        self.width = width
        self.decay = decay
        self.detectionMatrix = np.zeros((height, width), dtype=np.float32)  # Matriz conta as detecções em cada pixel
        self.logMatrix = np.zeros((height, width), dtype=np.float32)  # Transformação logarítmica da matriz de detecção
    
    def applyDecay(self):
        self.detectionMatrix *= self.decay
        self.logMatrix = np.log1p(self.detectionMatrix)  # Atualiza a matriz logaritimica
    
    def updateDetectionMatrix(self, bbox):
        x1, y1, x2, y2 = bbox
        
        # Incrementa a matriz de detecção na região da bounding box
        self.detectionMatrix[y1:y2, x1:x2] += 0.5
        
        # Atualiza a matriz logarítimica
        self.logMatrix = np.log1p(self.detectionMatrix)
    
    def getNormalizedDetectionMatrix(self):
        # Normaliza a matriz logarítmica para o intervalo [0, 255]
        normalizedMatrix = cv2.normalize(self.logMatrix, None, 0, 255, cv2.NORM_MINMAX)
        normalizedMatrix = 255 - normalizedMatrix  # Inverter a escala de cores
        return normalizedMatrix.astype(np.uint8)

    def getColoredHeatMap(self):
        normalizedMatrix = self.getNormalizedDetectionMatrix()
        heatmap = cv2.applyColorMap(normalizedMatrix, cv2.COLORMAP_JET)  # Aplicar mapa de cores
        return heatmap

    def overlayHeatMap(self, frame):
        #self.applyDecay()  # Aplica decaimento na matriz de detecção
        heatmap = self.getColoredHeatMap()
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)  
        output = cv2.addWeighted(frame, 0.6, heatmap, 0.4, 0)
        return output