# import the necessary packages
import numpy as np
import argparse
import cv2
import cv2


# load the image and convert it to grayscale
cap = cv2.VideoCapture(0)
searcher = 250
# Python 3 program for recursive binary search.
# Modifications needed for the older Python 2 are found in comments.

# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):

    # Check base case
    if high >= low:

        mid = (high + low) // 2

        # If element is present at the middle itself
        if arr(mid) == x:
            return mid

        # If element is smaller than mid, then it can only
        # be present in left subarray
        elif arr(mid) > x:
            return binary_search(arr, low, mid - 1, x)

        # Else the element can only be present in right subarray
        else:
            return binary_search(arr, mid + 1, high, x)

    else:
        # Element is not present in the array
        return -1


while True:
    _, image = cap.read()
    orig = image.copy()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_list = gray


        #if max(gray_list[i]) > 250:
        #print(gray[i])
    #break
    #print("Break-----")

    # for i in range(gray_list.shape[0]):     #traverse through height
    #     for j in range(gray_list.shape[1]): #traverse through width
    #         print(str(gray_list[i][j]), end=" ")
    #     print(" ")
    # for i in range(gray_list.shape[0]):  # traverse through height
    #     gray_list[i:].sort()
        # result = binary_search(gray_list[i:], 0, len(gray_list[i:]) - 1, searcher)
        # if result != -1:
        #     print("Element is present at index[" + str(i) + ":" + str(result) + "]")
        # else:
            #print("Element is not present in array")
    #break


    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False)
    ap.add_argument("-r", "--radius", type=int, help=3)
    args = vars(ap.parse_args())
    # perform a naive attempt to find the (x, y) coordinates of
    # the area of the image with the largest intensity value
    Max = np.amax(gray_list)
    #print("Max is = " + Max)

    if Max > 235:
        print("Shot is = " + str(Max))
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        cv2.circle(image, maxLoc, 5, (255, 0, 0), 2)
    # display the results of the naive attempt
    cv2.imshow("Naive", image)[]
    # apply a Gaussian blur to the image then find the brightest
    # region
    # gray = cv2.GaussianBlur(gray, (153, 5), 0)
    # (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    # image = orig.copy()
    # cv2.circle(image, maxLoc, args["radius"], (255, 0, 0), 2)
    # # display the results of our newly improved method
    # cv2.imshow("Robust", image)
    #cv2.waitKey(0)
    cv2.waitKey(1)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


