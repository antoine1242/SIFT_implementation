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

# TODO: si on veux: le chargé fit contraste avant extremum

def run():
    print("Project Pano is running!")
    
    print("Image 1")
    img_color = imread("./images/droite.jpg")
    img = rgb2gray(img_color)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
    print(type(img))
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, 3, 2)

    keypoints = detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])
    #for k in keypoints:
    #    print(k)
    # display_img_with_keypoints(img_color, keypoints)

    keypoints_descriptors1 = descriptionPointsCles(keypoints, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    print("Image 2")
    img_color = imread("./images/gauche.jpg")
    img = rgb2gray(img_color)

    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, 3, 2)

    keypoints = detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    keypoints_descriptors2 = descriptionPointsCles(keypoints, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

    print("Matrice de distance")
    distance_matrix = distance_inter_points(keypoints_descriptors1, keypoints_descriptors2)

    k_lowest = get_k_lowest(distance_matrix, 10)

    """
    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6+1):
        fig.add_subplot(2, 3, i)
        plt.imshow(gaussian_filtered_images[1][i-1], cmap='gray', vmin=0, vmax=1)
    plt.show()

    fig = plt.figure(figsize=(2,3))
    for i in range(1, 6):
        fig.add_subplot(2, 3, i)
        plt.imshow(dogs[1][i-1], cmap='gray', vmin=0, vmax=1)
    plt.show()
    """

    """
    previous = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])
    current = np.array([[9, 9, 9], [9, 8, 9], [9, 9, 9]])
    suivant = np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]])

    print(isExtremum(previous, current, suivant, 1, 1))
    """

def display_img_with_keypoints(img, keypoints):
    # Create a figure. Equal aspect so circles look circular
    fig,ax = plt.subplots(1)
    ax.set_aspect('equal')

    # Show the image
    ax.imshow(img)

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
