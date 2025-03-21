import numpy as np
import cv2

class Spaghetti:
    def __init__(self, frame_shape):
        self.frame_shape = frame_shape
        self.trajectory_points = {}  # Dictionary to store the trajectory points of each person

    def update(self, person, areas_dict):
        if person.positionHistory:  # Checks if the person has a position history
            centroid = person.positionHistory[-1]  # Last centroid of the person
            x, y = int(centroid[0]), int(centroid[1])  # Coordinates of the centroid

            if 0 <= y < self.frame_shape[0] and 0 <= x < self.frame_shape[1]:
                if person.visitedAreas:  #  Checks if the person has visited areas
                    first_area_name = person.visitedAreas[0]  # First area visited by the person
                    first_area = areas_dict.get(first_area_name)
                    if first_area:
                        color = first_area.color  # Cololr associated with the first area visited by the person

                        # Stores the centroid of the person in the trajectory matrix
                        if person.id not in self.trajectory_points:
                            self.trajectory_points[person.id] = {
                                "color": color,
                                "points": [],
                            }
                        self.trajectory_points[person.id]["points"].append((x, y))

    def drawSpaghetti(self, frame):
       
        overlayed_frame = frame

        # Draw lines conecting the points
        for person_id, data in self.trajectory_points.items():
            color = data["color"]
            points = data["points"]

            for i in range(1, len(points)):
                cv2.line(overlayed_frame, points[i - 1], points[i], color, thickness=2)

        # Display window with the spaghetti diagram
        cv2.imshow('Spaghetti Diagram', overlayed_frame)
        cv2.waitKey(1)

        return overlayed_frame