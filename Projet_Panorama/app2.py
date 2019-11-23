import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes
from descriptionPointsCles import descriptionPointsCles
from detectionPointsCles import detectionPointsCles, isExtremum
from matching import distance_inter_points
from matching import get_k_lowest
import cv2
from skimage.io import imread
from skimage.color import rgb2gray
from matplotlib.patches import Circle, Arrow
import math 
from detectionPointsCles import gaussian_filter
from scipy.ndimage.filters import convolve

def run():
    print("Project Pano is running App 2!")
    
    img_color1 = imread("./images/droite.jpg")
    img1 = rgb2gray(img_color1)

    # TODO: revoir s<il faut convoluer image initialement...
    # s0=1.3
    # img1 = convolve(img1, gaussian_filter(s0))

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img1, 3, 2)

    # for dog in dogs:
    #    print("dogs", dogs)

    keypoints1 = detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    keypoints_descriptors1 = descriptionPointsCles(keypoints1, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    display_img_with_keypoints(img_color1, keypoints1)
    


def display_img_with_keypoints(img, keypoints):
    # Create a figure. Equal aspect so circles look circular
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(img) # , cmap='Greys'

    # Now, loop through coord arrays, and create a circle at each x,y pair
    for keypoint in keypoints:
        x = keypoint[0]
        y = keypoint[1]
        r = 5 * keypoint[2]
        angle = math.radians(keypoint[3])
        dx = r * np.cos(angle)
        dy = r * np.sin(angle)

        line = Arrow(y, x, dx, dy, width=2.0)
        circ = Circle((y,x), r, fill=False)
        ax.add_patch(circ)
        ax.add_patch(line)

    # Show the image
    plt.show()

run()

