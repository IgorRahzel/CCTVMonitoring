import numpy as np
import cv2

class Spaghetti:
    def __init__(self, frame_shape):
        self.frame_shape = frame_shape
        self.trajectory_points = {}  # Dicionário para armazenar a trajetória de cada pessoa

    def update(self, person, areas_dict):
        if person.positionHistory:  # Caso pessoa tenha histórico de posições
            centroid = person.positionHistory[-1]  # Último centroíde da pessoa
            x, y = int(centroid[0]), int(centroid[1])  # Coordenadas do centroíde

            if 0 <= y < self.frame_shape[0] and 0 <= x < self.frame_shape[1]:
                if person.visitedAreas:  #  Caso a pessoa visitou alguma área
                    first_area_name = person.visitedAreas[0]  # Nome da primeira área visitada pela pessoa
                    first_area = areas_dict.get(first_area_name)
                    if first_area:
                        color = first_area.color  # Cor associada a primeira área visitada pela pessoa

                        # Armazena os centróides da pessoa no dicionário de trajetória
                        if person.id not in self.trajectory_points:
                            self.trajectory_points[person.id] = {
                                "color": color,
                                "points": [],
                            }
                        self.trajectory_points[person.id]["points"].append((x, y))

    def drawSpaghetti(self, frame):
       
        overlayed_frame = frame

        # Desenha as linhas da trajetória de cada pessoa
        for person_id, data in self.trajectory_points.items():
            color = data["color"]
            points = data["points"]

            for i in range(1, len(points)):
                cv2.line(overlayed_frame, points[i - 1], points[i], color, thickness=2)

        # Display window with the spaghetti diagram
        #cv2.imshow('Spaghetti Diagram', overlayed_frame)
        #cv2.waitKey(1)

        return overlayed_frame