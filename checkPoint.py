import cv2
import numpy as np


testListOfPoints = [[2, 2], [2, 3], [5, 3], [3.2, 4]]
R = 3.4   # Radius based on tolerance

def checkNewPoint(incomingPoint, listOfPoints):
    found = False

    if listOfPoints.__contains__([incomingPoint]):
        # This point is already in the list so we ignore
        print("Ignore")

    else:
        # This point is not in the array, let's check if it might belong to any circle
        for existingPoint in listOfPoints:
            # (x1 - x)^2 + (y1 - y)^2 < R ?
            if (pow(incomingPoint[0] - existingPoint[0], 2) + pow(incomingPoint[1] - existingPoint[1], 2)) < pow(R,2):
                # point is within a circle so we ignore it.
                print("Point is within the circle of center" + str(existingPoint) + " so we ignore it")
                found = True
                break

        if not found:
            # point not found within any radius, let's add it in the list
            listOfPoints.append(incomingPoint)
            print("Point " + str(incomingPoint) + " added in the list")
            return True
        else:
            # process completed
            print(" ")
            return False


checkNewPoint([5,4], testListOfPoints)