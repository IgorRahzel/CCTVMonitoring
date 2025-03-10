import cv2
import numpy as np

class heatMap:
    def __init__(self,height,width,decay = 0.2):
        self.height = height
        self.width = width
        self.decay = decay
        self._heatMap = np.zeros((height,width),dtype = np.float32)
    

    def updateHeatMap(self,bbox):
        self._heatMap *= self.decay

        x1,y1,x2,y2 = bbox
        self._heatMap[y1:y2,x1:x2] += 1
    
    def getColoredHeatMap(self):
        heatmap_norm = cv2.normalize(self._heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_uint8 = np.uint8(heatmap_norm)

        heatmap_colored = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        return heatmap_colored


    def overlayHeatMap(self,frame,alpha = 0.6):
        heatmap_colored = self.getColoredHeatMap()
        overlay = cv2.addWeighted(frame, alpha, heatmap_colored, 1 - alpha, 0)
        return overlay
