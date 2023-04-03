import numpy as np

file = open('ColorValues.txt','r')
read = file.readlines()
modified = []
temp = []

def findImgVAlues(activeScene):

    try:
        lowRed = np.array([0, 0, 0])
        upRed = np.array([0, 0, 0])
        isSceneActive = 0

        for line in read:
            modified.append(line.strip())

        for line in modified:
            temp = line.split('/')

            if temp[0] in activeScene:
                lowRed = np.array([int(temp[1]), int(temp[2]), int(temp[3])])
                upRed = np.array([int(temp[4]), int(temp[5]), int(temp[6])])
                isSceneActive = 1

        #if isSceneActive == 0:
            #print("No Active Scene.")

        return lowRed, upRed

    except Exception as e:
        print("ERROR:", e)
        pass
