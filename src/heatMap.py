import cv2
import numpy as np

class heatMap:
    def __init__(self, height, width, decay=0.99):
        self.height = height
        self.width = width
        self.decay = decay
        self.detectionMatrix = np.zeros((height, width), dtype=np.float32)  # Raw detection counts
        self.logMatrix = np.zeros((height, width), dtype=np.float32)  # Logarithmic transformation of detection counts
    
    def applyDecay(self):
        self.detectionMatrix *= self.decay
        self.logMatrix = np.log1p(self.detectionMatrix)  # Update log matrix after decay
    
    def updateDetectionMatrix(self, bbox):
        x1, y1, x2, y2 = bbox
        
        # Increment the detection matrix in the bounding box area
        self.detectionMatrix[y1:y2, x1:x2] += 1
        
        # Update the log matrix
        self.logMatrix = np.log1p(self.detectionMatrix)
        
        # Normalize the log matrix for visualization
        #normalized_matrix = cv2.normalize(self.logMatrix, None, 0, 255, cv2.NORM_MINMAX)
        #normalized_matrix = normalized_matrix.astype(np.uint8)  # Convert to 8-bit for display
        
        # Display the normalized log matrix
        #cv2.imshow('Log Detection Matrix', normalized_matrix)
    
    def getNormalizedDetectionMatrix(self):
        # Normalize the log matrix to the range 0-255
        normalizedMatrix = cv2.normalize(self.logMatrix, None, 0, 255, cv2.NORM_MINMAX)
        normalizedMatrix = 255 - normalizedMatrix  # Invert so blue is less and red is more
        return normalizedMatrix.astype(np.uint8)

    def getColoredHeatMap(self):
        normalizedMatrix = self.getNormalizedDetectionMatrix()
        heatmap = cv2.applyColorMap(normalizedMatrix, cv2.COLORMAP_JET)  # Apply the colormap
        return heatmap

    def overlayHeatMap(self, frame):
        self.applyDecay()  # Apply decay each iteration to smooth the transition
        heatmap = self.getColoredHeatMap()
        heatmap = cv2.cvtColor(heatmap, cv2.COLOR_BGR2RGB)  # Convert to the correct format
        output = cv2.addWeighted(frame, 0.6, heatmap, 0.4, 0)
        return output