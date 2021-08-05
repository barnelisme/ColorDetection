import numpy as np
import cv2

# Load image.
# img = cv2.imread ("images/BeeSimple.jpg")
# # Convert to grayscale.
# gray = cv2.cvtColor (img, cv2.COLOR_BGR2GRAY)
# # Binarize.
# thresh, binary = cv2.threshold (gray, 230, 255, cv2.THRESH_BINARY_INV)
# # Extract contours.
# contours, hierarchy = cv2.findContours (
#     binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
# )
# # Create a mask
# mask = np.zeros_like (binary)
# # Fill the outline (pixels not transparent) with 255.
# for cnt in contours:
#     cv2.drawContours (mask, contours, -1, color = 255, thickness = -1)
# # Convert to RGBA
# rgba = cv2.cvtColor (img, cv2.COLOR_RGB2RGBA)
# # Set the mask to the alpha channel.
# rgba [..., 3] = mask
# # Draw all outlines
# # cv2.drawContours (img, contours, -1, color = (0, 255, 0), thickness = 2)
# # save.
# cv2.imwrite ("images/BeeSimple2.png", rgba)
# # Display
# cv2.imshow ("img", rgba)
# cv2.waitKey (0)

def BallBehaviour (screenWidth, screenHeight, alive):
    ball_coordinates = np.random.randint(10,600,size=2)
    speed = np.random.randint(1, 7,size=1)
    # xb = 120
    # yb = 50
    x_mvmnt = "right"
    # Radius of circle
    radius = 10
    # Blue color in BGR
    ballcolor = (0, 0, 255)
    # Line thickness of 2 px
    ballThickness = 10
    return  ball_coordinates, speed, radius, ballcolor, ballThickness


def BallMovement(ballsMvmnt, ballsVerticalMvmnt, balls, frameWidth, frameHeight ):
    #print("Current Ball:", balls, " movement:", ballsMvmnt)
    x_mvmnt = ballsMvmnt
    y_mvmnt = ballsVerticalMvmnt
    xb, yb = balls[0]
    speed = balls[1]
    radius = balls[2]
    if x_mvmnt == "right":
        if xb < frameWidth - radius * 2:
            xb = xb + speed
        elif xb >= frameWidth - radius * 2:
            x_mvmnt = "left"
    else:
        if xb > 0:
            xb = xb - speed
        elif xb <= 0:
            x_mvmnt = "right"

    if y_mvmnt == "down":
        if yb < frameHeight - radius * 7:
            yb = yb + speed
        elif yb >= frameHeight - radius * 7:
            y_mvmnt = "up"
    else:
        if yb > 0:
            yb = yb - speed
        elif yb <= 0:
            y_mvmnt = "down"
    ball_coordinates = (xb, yb)
    #print("Ball movement:", y_mvmnt, "Coordinates:", xb, ":", yb)

    return x_mvmnt, y_mvmnt, ball_coordinates


def removeBGND():
    bgs = cv2.BackgroundSubtractorMOG2()
    capture = cv2.VideoCapture(0)
    cv2.namedWindow("Original", 1)
    cv2.namedWindow("Foreground", 1)
    while True:
        img = capture.read()[1]
    cv2.imshow("Original", img)
    fgmask = bgs.apply(img)
    foreground = cv2.bitwise_and(img, img, mask=fgmask)
    cv2.imshow("Foreground", foreground)
    if cv2.waitKey >= 27:
        cv2.destroyAllWindows()
    capture.release()