import cv2
import numpy as np

#load image with alpha channel.  use IMREAD_UNCHANGED to ensure loading of alpha channel
# image = cv2.imread('images/sunLogo.png', cv2.IMREAD_UNCHANGED)
#
# #make mask of where the transparent bits are
# trans_mask = image[:,:,3] == 0
#
# #replace areas of transparency with white and not transparent
# image[trans_mask] = [255, 255, 255, 255]
#
# #new image without alpha channel...
# new_img = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
#
# cv2.imshow("Trans",new_img)
#
# cv2.waitKey()
# cv2.destroyAllWindows()


############################################################################
# function to overlay a transparent image on background.
# def transparentOverlay(src, overlay, pos=(0, 0), scale=1):
#     """
#     :param src: Input Color Background Image
#     :param overlay: transparent Image (BGRA)
#     :param pos:  position where the image to be blit.
#     :param scale : scale factor of transparent image.
#     :return: Resultant Image
#     """
#     overlay = cv2.resize(overlay, (0, 0), fx=scale, fy=scale)
#     h, w, _ = overlay.shape  # Size of foreground
#     rows, cols, _ = src.shape  # Size of background Image
#     y, x = pos[0], pos[1]  # Position of foreground/overlay image
#
#     # loop over all pixels and apply the blending equation
#     for i in range(h):
#         for j in range(w):
#             if x + i >= rows or y + j >= cols:
#                 continue
#             alpha = float(overlay[i][j][3] / 255.0)  # read the alpha channel
#             src[x + i][y + j] = alpha * overlay[i][j][:3] + (1 - alpha) * src[x + i][y + j]
#     return src
#
#
# # read all images
# bImg = cv2.imread("images/back.png")
#
# # KeyPoint : Remember to use cv2.IMREAD_UNCHANGED flag to load the image with alpha channel
# overlayImage = cv2.imread("images/sunLogo.png", cv2.IMREAD_UNCHANGED)
# logoImage = cv2.imread("images/back.png", cv2.IMREAD_UNCHANGED)
#
# # Overlay transparent images at desired postion(x,y) and Scale.
# result = transparentOverlay(bImg, overlayImage, (300, 0), 0.7)
# result = transparentOverlay(bImg, logoImage, (800, 400), 2)
#
# # Display the result
# cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
# cv2.imshow("Result", result)
# cv2.waitKey()
# cv2.destroyAllWindows()