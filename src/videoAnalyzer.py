from area import area
from person import person
from heatMap import heatMap
import cv2
import numpy as np

class videoAnalyzer:
    def __init__(self,areasList,height,width):
        self.id = 0
        self.areasDict = self._buildAreasDict(areasList)
        self.people = {}
        self.heatmap = heatMap(height,width)

    def _buildAreasDict(self,areasList):
        areasDict = {}
        for area in areasList:
            areasDict[area.name] = area
        return areasDict
        
    # Return tuple of BBOx and centroids
    def getData(self,results):
        data = []
        for box in results[0].boxes:
            cls = int(box.cls[0])
            if cls == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                data.append(((x1, y1, x2, y2), ((x1 + x2) // 2, (y1 + y2) // 2)))
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
        for coordinates,centroid in data:
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
                self.people[closest_person].lastFrameDetected = frameNumber
            # If the centroid wasn't close to any person in the dictionary, create a new person
            else:
                self.id += 1
                self.people[self.id] = person(self.id,frameNumber)
                self.people[self.id].updatePosition(coordinates,centroid)


    def updatePersonArea(self):
        for person in self.people.values():
            for _area in self.areasDict.values():
                val = _area.isInside(person.positionHistory[-1])
                if val > 0:
                    person.currentArea = _area.name
                    break
    

    def updateAreas(self):
        for id,_person in self.people.items():
            if _person.currentArea is not None:
                self.areasDict[_person.currentArea].currentIdsInArea.append(id)
                self.areasDict[_person.currentArea].IdsRecordInArea.add(id)
                self.areasDict[_person.currentArea].currentNumberOfPeople += 1
                self.areasDict[_person.currentArea].totalNumberOfPeople = len(self.areasDict[_person.currentArea].IdsRecordInArea)

    
    def drawBoundingBoxes(self,frame):
        for _person in self.people.values():
            x1,y1,x2,y2 = _person.BBox
            cv2.rectangle(frame, (x1, y1), (x2, y2), _person.BBoxColor, 2)
            cv2.putText(frame, f'id:{_person.id}', (x1, y1-3),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame
    

    def drawAreas(self, frame):
        for _area in self.areasDict.values():
            # Desenha o polígono da área
            cv2.polylines(frame, [np.array(_area.vertices)], True, _area.color, 2)
            
            # Obtém os vértices do polígono
            vertices = np.array(_area.vertices)
            
            # Encontra o ponto superior direito (menor y e maior x)
            top_right_point = vertices[np.argmin(vertices[:, 1])]  # Ponto com o menor y
            # Se houver múltiplos pontos com o mesmo y, escolha o que tem o maior x
            top_right_candidates = vertices[vertices[:, 1] == top_right_point[1]]
            top_right_point = top_right_candidates[np.argmin(top_right_candidates[:, 0])]
            
            # Define a posição do texto: abaixo e à direita do ponto superior direito
            text_x = top_right_point[0] + 5  # Mesmo x do ponto superior direito
            text_y = top_right_point[1] + 10  # Ajuste para colocar o texto abaixo do ponto

            # Escreve o nome da área e a quantidade de pessoas
            text = f'{_area.name}'
            cv2.putText(frame, text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        
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
        self.clearAreaCurrentInfo()

        return frame

    

                