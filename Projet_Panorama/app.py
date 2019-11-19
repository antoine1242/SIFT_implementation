import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from difference_de_gaussiennes import difference_de_gaussiennes
from detectionPointsCles import detectionPointsCles, isExtremum
import cv2
from skimage.io import imread
from skimage.color import rgb2gray

def run():
    print("Project Pano is running!")
    
    img = imread("./images/droite.jpg")
    img = rgb2gray(img)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    """
    print(type(img))
    cv2.imshow('image',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    """
    dogs, sigmas, gaussian_filtered_images, gaussian_filtered_images_sigmas = difference_de_gaussiennes(img, 3, 2)

    detectionPointsCles(dogs[0], sigmas[0], 0.03, 10, 0, gaussian_filtered_images[0], gaussian_filtered_images_sigmas[0])

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
run()
